# Generated by Django 5.0.2 on 2025-02-04 18:48

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_tag', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('manufacturer', models.CharField(max_length=100)),
                ('model_number', models.CharField(max_length=100)),
                ('serial_number', models.CharField(max_length=100, unique=True)),
                ('purchase_date', models.DateField()),
                ('purchase_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('warranty_expiry', models.DateField()),
                ('status', models.CharField(choices=[('available', 'Available'), ('in_use', 'In Use'), ('maintenance', 'Under Maintenance'), ('retired', 'Retired')], default='available', max_length=20)),
                ('location', models.CharField(max_length=200)),
                ('qr_code', models.ImageField(blank=True, upload_to='qr_codes/')),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='AssetAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkout_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('expected_return_date', models.DateTimeField(blank=True, null=True)),
                ('return_date', models.DateTimeField(blank=True, null=True)),
                ('condition_on_checkout', models.TextField()),
                ('condition_on_return', models.TextField(blank=True)),
                ('notes', models.TextField(blank=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.asset')),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('checked_out_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='checkout_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='asset',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.category'),
        ),
        migrations.CreateModel(
            name='MaintenanceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maintenance_type', models.CharField(choices=[('preventive', 'Preventive Maintenance'), ('corrective', 'Corrective Maintenance'), ('upgrade', 'Upgrade')], max_length=20)),
                ('maintenance_date', models.DateTimeField()),
                ('performed_by', models.CharField(max_length=100)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('next_maintenance_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.asset')),
            ],
        ),
    ]
