from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Creates a superuser if one does not exist'

    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():
            try:
                User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password='admin123'
                )
                self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
            except IntegrityError:
                self.stdout.write(self.style.ERROR('Superuser creation failed'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists')) 