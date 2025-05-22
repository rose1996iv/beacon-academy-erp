# Deployment Guide

This guide covers the deployment process for the Beacon Academy ERP System.

## Prerequisites

- Python 3.10 or higher
- PostgreSQL 13.0 or higher (for production)
- Nginx (for production)
- SSL certificate (for production)

## Development Deployment

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd erp
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Unix/macOS
   .\venv\Scripts\Activate   # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update the variables with your configuration

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Production Deployment

### Server Setup

1. Update the system:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. Install required packages:
   ```bash
   sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib
   ```

### Database Setup

1. Create a PostgreSQL database and user:
   ```sql
   CREATE DATABASE beaconerp;
   CREATE USER beaconuser WITH PASSWORD 'your_password';
   ALTER ROLE beaconuser SET client_encoding TO 'utf8';
   ALTER ROLE beaconuser SET default_transaction_isolation TO 'read committed';
   ALTER ROLE beaconuser SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE beaconerp TO beaconuser;
   ```

2. Update settings.py with PostgreSQL configuration:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'beaconerp',
           'USER': 'beaconuser',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

### Application Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd erp
   ```

2. Set up virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install production requirements:
   ```bash
   pip install -r requirements.txt
   pip install gunicorn psycopg2-binary
   ```

4. Configure environment variables:
   - Create .env file with production settings
   - Set DEBUG=False
   - Update ALLOWED_HOSTS
   - Set secure SECRET_KEY

5. Set up static files:
   ```bash
   python manage.py collectstatic
   ```

### Gunicorn Setup

1. Create a systemd service file:
   ```ini
   [Unit]
   Description=Beacon Academy ERP Gunicorn Daemon
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/path/to/erp
   ExecStart=/path/to/erp/venv/bin/gunicorn --workers 3 --bind unix:/run/beaconerp.sock beaconerp.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```

2. Enable and start the service:
   ```bash
   sudo systemctl enable beaconerp
   sudo systemctl start beaconerp
   ```

### Nginx Configuration

1. Create Nginx configuration:
   ```nginx
   server {
       listen 80;
       server_name your_domain.com;
       return 301 https://$server_name$request_uri;
   }

   server {
       listen 443 ssl;
       server_name your_domain.com;

       ssl_certificate /path/to/ssl/certificate;
       ssl_certificate_key /path/to/ssl/private_key;

       location = /favicon.ico { access_log off; log_not_found off; }
       
       location /static/ {
           root /path/to/erp;
       }

       location /media/ {
           root /path/to/erp;
       }

       location / {
           include proxy_params;
           proxy_pass http://unix:/run/beaconerp.sock;
       }
   }
   ```

2. Test and restart Nginx:
   ```bash
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## Security Considerations

1. Enable SSL/TLS
2. Set up firewall rules
3. Configure secure headers
4. Enable regular backups
5. Set up monitoring

## Maintenance

1. Regular updates:
   ```bash
   git pull origin main
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic
   sudo systemctl restart beaconerp
   ```

2. Backup database:
   ```bash
   pg_dump beaconerp > backup_$(date +%Y%m%d).sql
   ```

3. Monitor logs:
   ```bash
   sudo journalctl -u beaconerp
   ```

## Troubleshooting

Common issues and their solutions:

1. Static files not showing:
   - Check STATIC_ROOT setting
   - Run collectstatic
   - Verify Nginx configuration

2. 502 Bad Gateway:
   - Check Gunicorn service status
   - Verify socket permissions
   - Check error logs

3. Database connection issues:
   - Verify PostgreSQL service status
   - Check database credentials
   - Confirm firewall rules

For more detailed troubleshooting, check the application logs in `/var/log/beaconerp/`.
