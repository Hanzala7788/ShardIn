# ShardIn AWS Ubuntu VM Deployment Guide (Docker)

## Prerequisites

Before deploying, ensure your AWS Ubuntu VM has the following installed:

### 1. System Updates

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install Docker and Docker Compose

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group (to run docker without sudo)
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose-plugin -y

# Verify installations
docker --version
docker compose version
```

### 3. Install Git

```bash
sudo apt install -y git
```

## Initial Server Setup

### 1. Clone Repository

```bash
cd ~
git clone https://github.com/Hanzala7788/ShardIn.git
cd ShardIn
```

### 2. Configure Environment Variables

```bash
# Create .env file with your settings
nano .env
```

Add your environment variables (use `.env.example` as reference):

```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com,your-ip-address

# Database settings
DB_NAME=shardin_db
DB_USER=shardin_user
DB_USER_PASSWORD=your_secure_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Add other environment variables as needed
EOF
```

### 3. Start the Application with Docker Compose

```bash
# Build and start all services (web, db, pgadmin)
docker compose up -d --build

# Wait for services to start
sleep 10

# Run initial migrations
docker compose exec web python manage.py migrate

# Create superuser (interactive)
docker compose exec web python manage.py createsuperuser

# Collect static files
docker compose exec web python manage.py collectstatic --noinput

# Check running containers
docker compose ps
```

### 4. Configure Nginx Reverse Proxy (Optional but Recommended)

```bash
# Install Nginx
sudo apt install nginx -y

# Create Nginx configuration
sudo nano /etc/nginx/sites-available/shardin
```

Add this configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com your-ip-address;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /home/ubuntu/ShardIn/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/shardin /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## GitHub Secrets Configuration

Add these secrets to your GitHub repository (`Settings` → `Secrets and variables` → `Actions`):

1. **`AWS_HOST`** - Your EC2 instance public IP or domain

   ```
   ec2-xx-xx-xx-xx.compute-1.amazonaws.com
   ```

2. **`AWS_USER`** - SSH username (usually `ubuntu` for Ubuntu AMI)

   ```
   ubuntu
   ```

3. **`AWS_SSH_KEY`** - Your private SSH key

   ```
   -----BEGIN RSA PRIVATE KEY-----
   [Your private key content]
   -----END RSA PRIVATE KEY-----
   ```

4. **`AWS_PORT`** - SSH port (optional, defaults to 22)
   ```
   22
   ```

## AWS Security Group Configuration

Ensure your EC2 security group allows:

- **SSH (22)** - From your IP or GitHub Actions IPs
- **HTTP (80)** - From anywhere (0.0.0.0/0)
- **HTTPS (443)** - From anywhere (0.0.0.0/0) if using SSL
- **Custom TCP (8000)** - From localhost only (for testing)

## Deployment Process

Once everything is set up:

1. Push code to `main` branch
2. GitHub Actions will automatically:
   - Connect to your VM via SSH
   - Pull latest code
   - Install dependencies
   - Run migrations
   - Collect static files
   - Restart the service
   - Verify deployment

## Manual Deployment Commands

If you need to deploy manually:

```bash
# SSH into your server
ssh ubuntu@your-ec2-instance

# Navigate to project
cd ~/ShardIn

# Pull latest changes
git pull origin main

# Stop containers
docker compose down

# Rebuild and start containers
docker compose up -d --build

# Run migrations
docker compose exec web python manage.py migrate --noinput

# Collect static files
docker compose exec web python manage.py collectstatic --noinput

# Check container status
docker compose ps

# View logs
docker compose logs -f web
```

## Troubleshooting

### Check Application Logs

```bash
# View all logs
docker compose logs

# View web container logs
docker compose logs web

# Follow logs in real-time
docker compose logs -f web

# View last 50 lines
docker compose logs --tail=50 web
```

### Check Database Logs

```bash
docker compose logs db
```

### Restart Services

```bash
# Restart all services
docker compose restart

# Restart specific service
docker compose restart web
docker compose restart db
```

### Check Container Status

```bash
docker compose ps
```

### Access Container Shell

```bash
# Access web container
docker compose exec web bash

# Access database
docker compose exec db psql -U postgres -d jotit
```

### Clean Up

```bash
# Stop and remove containers
docker compose down

# Remove volumes (WARNING: deletes database data)
docker compose down -v

# Remove unused images
docker image prune -f
```

## SSL/HTTPS Setup (Recommended)

Install Certbot for free SSL certificates:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## Monitoring

Set up monitoring with:

```bash
# Install htop for system monitoring
sudo apt install htop

# Monitor application
htop
```

## Backup Strategy

Create regular backups:

```bash
# Database backup
pg_dump -U shardin_user shardin_db > backup_$(date +%Y%m%d).sql

# Code backup (already in Git)
git push origin main
```
