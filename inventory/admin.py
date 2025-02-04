from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .models import Category, Asset, AssetAssignment, MaintenanceRecord
from .views import import_assets

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_tag', 'name', 'category', 'status', 'location', 'purchase_date', 'warranty_expiry')
    list_filter = ('status', 'category', 'location')
    search_fields = ('asset_tag', 'name', 'description', 'serial_number')
    ordering = ('asset_tag',)
    date_hierarchy = 'purchase_date'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(import_assets), name='inventory_asset_import'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_import_button'] = True
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(AssetAssignment)
class AssetAssignmentAdmin(admin.ModelAdmin):
    list_display = ('asset', 'assigned_to', 'checkout_date', 'expected_return_date', 'return_date')
    list_filter = ('checkout_date', 'return_date')
    search_fields = ('asset__asset_tag', 'asset__name', 'assigned_to__username')
    ordering = ('-checkout_date',)
    date_hierarchy = 'checkout_date'

@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ('asset', 'maintenance_type', 'maintenance_date', 'performed_by', 'cost', 'next_maintenance_date')
    list_filter = ('maintenance_type', 'maintenance_date')
    search_fields = ('asset__asset_tag', 'asset__name', 'performed_by')
    ordering = ('-maintenance_date',)
    date_hierarchy = 'maintenance_date'
