from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Asset(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired'),
    ]

    asset_tag = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    manufacturer = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    purchase_date = models.DateField()
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2)
    warranty_expiry = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    location = models.CharField(max_length=200)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.asset_tag} - {self.name}"

    def save(self, *args, **kwargs):
        # Generate QR code if it doesn't exist
        if not self.qr_code:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(f'Asset Tag: {self.asset_tag}\nSerial: {self.serial_number}')
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            self.qr_code.save(f'qr_{self.asset_tag}.png', File(buffer), save=False)

        super().save(*args, **kwargs)

class AssetAssignment(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)
    assigned_to = models.ForeignKey(User, on_delete=models.PROTECT)
    checked_out_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='checkout_user')
    checkout_date = models.DateTimeField(default=timezone.now)
    expected_return_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)
    condition_on_checkout = models.TextField()
    condition_on_return = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.asset} - {self.assigned_to}"

class MaintenanceRecord(models.Model):
    MAINTENANCE_TYPE_CHOICES = [
        ('preventive', 'Preventive Maintenance'),
        ('corrective', 'Corrective Maintenance'),
        ('upgrade', 'Upgrade'),
    ]

    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)
    maintenance_type = models.CharField(max_length=20, choices=MAINTENANCE_TYPE_CHOICES)
    maintenance_date = models.DateTimeField()
    performed_by = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    next_maintenance_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.asset} - {self.maintenance_type} - {self.maintenance_date}"
