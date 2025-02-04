from django.utils import timezone
from datetime import datetime, timedelta
from inventory.models import Category, Asset
from django.contrib.auth.models import User

# Create categories
def create_categories():
    categories = {
        'Laptops': 'Company laptops for employee use',
        'Peripherals': 'Computer peripherals like keyboards, mice, etc.',
        'Phones': 'Office desk phones and communication devices',
        'Desktops': 'Desktop computers and workstations',
    }
    
    created_categories = {}
    for name, desc in categories.items():
        cat, created = Category.objects.get_or_create(
            name=name,
            defaults={'description': desc}
        )
        created_categories[name] = cat
    return created_categories

# Create assets
def create_assets(categories):
    # New Laptops
    new_laptops = [
        {
            'asset_tag': 'LAP-2024-001',
            'name': 'Dell Latitude 5430',
            'manufacturer': 'Dell',
            'model_number': 'LAT5430',
            'status': 'available'
        },
        {
            'asset_tag': 'LAP-2024-002',
            'name': 'Dell Latitude 5430',
            'manufacturer': 'Dell',
            'model_number': 'LAT5430',
            'status': 'available'
        },
        {
            'asset_tag': 'LAP-2024-003',
            'name': 'Dell Latitude 5430',
            'manufacturer': 'Dell',
            'model_number': 'LAT5430',
            'status': 'available'
        }
    ]

    # Old Laptops
    old_laptops = [
        {
            'asset_tag': 'LAP-2022-001',
            'name': 'Dell Latitude 5410',
            'manufacturer': 'Dell',
            'model_number': 'LAT5410',
            'status': 'in_use'
        },
        {
            'asset_tag': 'LAP-2022-002',
            'name': 'Dell Latitude 5410',
            'manufacturer': 'Dell',
            'model_number': 'LAT5410',
            'status': 'in_use'
        }
    ]

    # Peripherals (Mouse and Keyboard Combos)
    peripherals = [
        {
            'asset_tag': f'PER-2024-{str(i).zfill(3)}',
            'name': 'Logitech MK270 Wireless Combo',
            'manufacturer': 'Logitech',
            'model_number': 'MK270',
            'status': 'available'
        } for i in range(1, 7)
    ]

    # Desk Phones
    phones = [
        {
            'asset_tag': f'PHO-2024-{str(i).zfill(3)}',
            'name': 'Cisco IP Phone 8841',
            'manufacturer': 'Cisco',
            'model_number': 'CP-8841-K9',
            'status': 'available'
        } for i in range(1, 5)
    ]

    # Old Desktops
    old_desktops = [
        {
            'asset_tag': f'DSK-2021-{str(i).zfill(3)}',
            'name': 'Dell OptiPlex 7060',
            'manufacturer': 'Dell',
            'model_number': 'OPT7060',
            'status': 'retired'
        } for i in range(1, 9)
    ]

    # Common asset details
    purchase_date = datetime.now().date() - timedelta(days=30)  # For new items
    old_purchase_date = datetime.now().date() - timedelta(days=730)  # For old items
    warranty_new = datetime.now().date() + timedelta(days=1095)  # 3 years for new items
    warranty_old = datetime.now().date() - timedelta(days=365)  # Expired warranty for old items

    # Create all assets
    def create_asset_batch(items, category, is_new=True):
        for item in items:
            Asset.objects.get_or_create(
                asset_tag=item['asset_tag'],
                defaults={
                    'name': item['name'],
                    'category': category,
                    'manufacturer': item['manufacturer'],
                    'model_number': item['model_number'],
                    'serial_number': f"SN-{item['asset_tag']}",  # Generate a unique serial number
                    'purchase_date': purchase_date if is_new else old_purchase_date,
                    'purchase_cost': 1200.00 if 'LAP' in item['asset_tag'] else 
                                   800.00 if 'DSK' in item['asset_tag'] else
                                   80.00 if 'PER' in item['asset_tag'] else
                                   200.00,  # For phones
                    'warranty_expiry': warranty_new if is_new else warranty_old,
                    'status': item['status'],
                    'location': 'Main Office',
                    'description': f"Company {item['name']} - {item['status']}"
                }
            )

    # Create assets by category
    create_asset_batch(new_laptops, categories['Laptops'])
    create_asset_batch(old_laptops, categories['Laptops'], False)
    create_asset_batch(peripherals, categories['Peripherals'])
    create_asset_batch(phones, categories['Phones'])
    create_asset_batch(old_desktops, categories['Desktops'], False)

if __name__ == '__main__':
    categories = create_categories()
    create_assets(categories)
    print("Initial inventory has been created successfully!") 