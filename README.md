# IT Equipment Inventory Management System

A web-based IT inventory tracking system built with Django, designed for IT departments, system administrators, and asset managers.

## Features

- Asset tracking with QR code generation
- Asset lifecycle management
- Check-in/Check-out system
- Maintenance records
- Reporting capabilities
- User authentication and authorization

## Prerequisites

- Python 3.8+
- Microsoft SQL Server
- ODBC Driver 17 for SQL Server

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd InventoryApp
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
# OR
source venv/bin/activate  # On Unix/MacOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and configure your environment variables:
```
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=inventory_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=1433
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. Create the database in SQL Server:
```sql
CREATE DATABASE inventory_db;
```

6. Apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

7. Create a superuser:
```bash
python manage.py create_superuser
```

8. Run the development server:
```bash
python manage.py runserver
```

The application will be available at http://localhost:8000

## Default Superuser Credentials

- Username: admin
- Password: admin123
- Email: admin@example.com

**Note:** Please change these credentials immediately after first login.

## Usage

1. Log in to the admin interface at http://localhost:8000/admin
2. Create categories for your assets
3. Add assets with their details
4. Manage asset assignments and maintenance records
5. Generate QR codes for asset tracking

## Directory Structure

```
InventoryApp/
├── inventory/              # Main application
│   ├── migrations/        # Database migrations
│   ├── management/        # Custom management commands
│   ├── models.py         # Database models
│   ├── admin.py         # Admin interface configuration
│   └── ...
├── inventory_project/     # Project configuration
├── static/               # Static files
├── media/                # User-uploaded files
├── templates/            # HTML templates
├── requirements.txt      # Project dependencies
└── manage.py            # Django management script
```

## Security Considerations

1. Change the default superuser password immediately
2. Use strong passwords for database and Django admin
3. Keep the SECRET_KEY secure and unique
4. Configure ALLOWED_HOSTS appropriately for production
5. Enable HTTPS in production

## Backup and Maintenance

1. Regular database backups
2. Keep dependencies updated
3. Monitor disk space for media files
4. Regular security updates

## License

This project is licensed under the MIT License - see the LICENSE file for details. 