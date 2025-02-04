from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
import csv
from datetime import datetime
from .models import Asset, Category
import os
from django.conf import settings

# Create your views here.

@staff_member_required
def download_asset_template(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'templates', 'asset_import_template.csv')
    response = FileResponse(open(file_path, 'rb'), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="asset_template.csv"'
    return response

@staff_member_required
def import_assets(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a CSV file.')
            return redirect('admin:inventory_asset_changelist')
        
        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            
            for row in reader:
                try:
                    # Print row data for debugging
                    print(f"Processing row {reader.line_num}: {row}")
                    
                    # Get or create category (this will create the category if it doesn't exist)
                    if 'category' not in row:
                        raise ValueError(f"'category' field is missing. Available fields: {list(row.keys())}")
                    
                    category_name = row['category'].strip()
                    if not category_name:
                        raise ValueError("Category name cannot be empty")
                        
                    print(f"Attempting to create/get category: '{category_name}'")
                    
                    category, created = Category.objects.get_or_create(
                        name=category_name,
                        defaults={'description': f'Auto-created category for {category_name}'}
                    )
                    
                    print(f"Category {'created' if created else 'found'}: {category.name}")
                    
                    # Create asset with only the fields from the template
                    Asset.objects.create(
                        asset_tag=row['asset_tag'].strip(),
                        name=row['name'].strip(),
                        description=row['description'].strip(),
                        category=category,
                        manufacturer=row['manufacturer'].strip(),
                        model_number=row['model_number'].strip(),
                        status=row['status'].strip(),
                        purchase_cost=float(row['purchase_cost']) if row['purchase_cost'].strip() else 0.0,
                        location=row['location'].strip(),
                        notes=row['notes'].strip(),
                        # Set default values for required fields that are not in template
                        purchase_date=datetime.now().date(),
                        warranty_expiry=datetime.now().date(),
                        serial_number=f"AUTO-{row['asset_tag'].strip()}"  # Generate a default serial number based on asset tag
                    )
                except Exception as e:
                    messages.error(request, f'Error in row {reader.line_num}: {str(e)}. Row data: {row}')
                    continue
            
            messages.success(request, 'Assets imported successfully!')
        except Exception as e:
            messages.error(request, f'Error processing file: {str(e)}')
        
        return redirect('admin:inventory_asset_changelist')
    
    return render(request, 'admin/inventory/asset/import_csv.html')
