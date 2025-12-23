# ShardIn Deployment Documentation

Complete guide for deploying the ShardIn Django application to AWS EC2 using Docker and GitHub Actions.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Initial Server Setup](#initial-server-setup)
4. [GitHub Actions Configuration](#github-actions-configuration)
5. [Deployment Workflow](#deployment-workflow)
6. [Manual Deployment](#manual-deployment)
7. [Troubleshooting](#troubleshooting)
8. [Useful Commands](#useful-commands)

---

## Overview

### Architecture

```
┌─────────────────┐
│  GitHub Repo    │
│   (dev branch)  │
└────────┬────────┘
         │ git push
         ▼
┌─────────────────┐
│ GitHub Actions  │
│   CI/CD Pipeline│
└────────┬────────┘
         │ SSH Deploy
         ▼
┌─────────────────┐
│  AWS EC2 Ubuntu │
│  ┌───────────┐  │
│  │  Docker   │  │
│  │ Compose   │  │
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │PostgreSQL │  │
│  │  Django   │  │
│  │  PgAdmin  │  │
│  └───────────┘  │
└─────────────────┘
```

### Technology Stack

- **Application**: Django 5.2.0 + Django REST Framework
- **Web Server**: Gunicorn (4 workers)
- **Database**: PostgreSQL 15
- **Containerization**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Server**: AWS EC2 Ubuntu
- **Reverse Proxy**: Nginx (optional)

---

## Prerequisites

### Local Development Machine

- Git installed
- SSH key for AWS EC2 (`ShadIn.pem`)
- GitHub account with repository access

### AWS EC2 Instance

- **OS**: Ubuntu 22.04 or later
- **Instance Type**: t2.micro or better
- **Storage**: At least 8GB
- **Security Group**: Ports 22, 80, 8080, 5050 open
- **Elastic IP**: Recommended for production

---

## Initial Server Setup

### Step 1: Connect to EC2

```bash
# SSH into your EC2 instance
ssh -i /path/to/ShadIn.pem ubuntu@13.60.157.187
```

### Step 2: Install Docker

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Docker using the official script
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add current user to docker group
sudo usermod -aG docker ubuntu

# Install Docker Compose plugin
sudo apt install -y docker-compose-plugin

# Verify installations
docker --version
docker compose version
```

### Step 3: Install Git

```bash
sudo apt install -y git
```

### Step 4: Clone Repository

```bash
# Clone the repository
cd ~
git clone https://github.com/Hanzala7788/ShardIn.git
cd ShardIn

# Checkout dev branch
git checkout dev
```

### Step 5: Configure Environment

```bash
# Create .env file
nano .env
```

Add the following configuration:

```env
# Django Settings
DEBUG=False
SECRET_KEY=your-secret-key-here-change-this
ALLOWED_HOSTS=["127.0.0.1", "13.60.157.187", "localhost", "your-domain.com"]

# Database Configuration (must match docker-compose.yaml)
DB_NAME=jotit
DB_USER=postgres
DB_USER_PASSWORD=your_secure_password_here
DATABASE_HOST=db
DATABASE_PORT=5432

# PgAdmin Configuration
PGADMIN_EMAIL=admin@local.com
PGADMIN_PASSWORD=admin
```

**Important**: Change `SECRET_KEY` and `DB_USER_PASSWORD` to secure values!

### Step 6: Initial Deployment

```bash
# Build and start containers
docker compose up -d --build

# Wait for services to start
sleep 15

# Run migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

# Collect static files
docker compose exec web python manage.py collectstatic --noinput

# Verify all containers are running
docker compose ps
```

### Step 7: Log Out and Back In

```bash
# Exit SSH session
exit

# Reconnect (to apply docker group permissions)
ssh -i /path/to/ShadIn.pem ubuntu@13.60.157.187
```

---

## GitHub Actions Configuration

### Step 1: Add Repository Secrets

Go to: `https://github.com/Hanzala7788/ShardIn/settings/secrets/actions`

Click **"New repository secret"** and add each of these:

#### AWS_HOST

- **Name**: `AWS_HOST`
- **Value**: `13.60.157.187` (your EC2 public IP)

#### AWS_USER

- **Name**: `AWS_USER`
- **Value**: `ubuntu`

#### AWS_SSH_KEY

- **Name**: `AWS_SSH_KEY`
- **Value**: Complete content of your `ShadIn.pem` file

```bash
# Display your PEM file content
cat /path/to/ShadIn.pem
```

Copy everything including:

```
-----BEGIN RSA PRIVATE KEY-----
...
-----END RSA PRIVATE KEY-----
```

#### AWS_PORT (Optional)

- **Name**: `AWS_PORT`
- **Value**: `22`

### Step 2: Configure Environment in GitHub

1. Go to `Settings` → `Environments`
2. Create environment named `env`
3. Add the same secrets to the environment

### Step 3: Verify Workflow File

The workflow file is located at `.github/workflows/deploy.yml`

**Triggers**:

- Push to `dev` branch
- Manual trigger via GitHub Actions UI

**Steps**:

1. Checkout code
2. Verify secrets are configured
3. SSH to EC2 server
4. Pull latest code from `dev` branch
5. Rebuild Docker containers
6. Run migrations
7. Collect static files
8. Verify deployment

---

## Deployment Workflow

### Automatic Deployment

Every time you push to the `dev` branch, the application automatically deploys:

```bash
# 1. Make your code changes
# Edit files...

# 2. Stage changes
git add .

# 3. Commit changes
git commit -m "Your descriptive commit message"

# 4. Push to dev branch
git push origin dev

# 5. GitHub Actions automatically deploys!
# Monitor at: https://github.com/Hanzala7788/ShardIn/actions
```

### Manual Deployment Trigger

1. Go to `https://github.com/Hanzala7788/ShardIn/actions`
2. Click "Deploy to Amazon Ubuntu VM"
3. Click "Run workflow"
4. Select `dev` branch
5. Click "Run workflow"

### Deployment Timeline

- **Trigger**: Instant (on git push)
- **Build**: ~30-60 seconds
- **Deploy**: ~30-60 seconds
- **Total**: ~1-2 minutes

---

## Manual Deployment

If you need to deploy manually without GitHub Actions:

### SSH into Server

```bash
ssh -i /path/to/ShadIn.pem ubuntu@13.60.157.187
cd ~/ShardIn
```

### Pull Latest Code

```bash
# Discard local changes and pull
git reset --hard
git pull origin dev
```

### Rebuild and Restart

```bash
# Stop containers
docker compose down

# Remove old images
docker image prune -f

# Rebuild and start
docker compose up -d --build

# Wait for services
sleep 15

# Run migrations
docker compose exec web python manage.py migrate --noinput

# Collect static files
docker compose exec web python manage.py collectstatic --noinput

# Check status
docker compose ps
```

---

## Troubleshooting

### Check Container Status

```bash
# View all containers
docker compose ps

# View specific container
docker compose ps web
```

### View Logs

```bash
# View all logs
docker compose logs

# View web container logs
docker compose logs web

# Follow logs in real-time
docker compose logs -f web

# View last 50 lines
docker compose logs --tail=50 web

# View database logs
docker compose logs db
```

### Container Not Starting

```bash
# Check detailed logs
docker compose logs web

# Restart specific container
docker compose restart web

# Rebuild specific container
docker compose up -d --build web
```

### Database Connection Issues

```bash
# Check database logs
docker compose logs db

# Verify database is running
docker compose ps db

# Restart database
docker compose restart db

# Access database shell
docker compose exec db psql -U postgres -d jotit
```

### Git Pull Conflicts

```bash
# On EC2 server
cd ~/ShardIn

# Discard local changes
git reset --hard

# Pull latest
git pull origin dev
```

### Permission Denied Errors

```bash
# Add user to docker group
sudo usermod -aG docker ubuntu

# Log out and back in
exit
ssh -i /path/to/ShadIn.pem ubuntu@13.60.157.187
```

### Application Not Accessible

1. **Check containers are running**:

   ```bash
   docker compose ps
   ```

2. **Check security group**:

   - Port 8080 must be open
   - Source: `0.0.0.0/0`

3. **Check application logs**:

   ```bash
   docker compose logs web
   ```

4. **Test locally on server**:
   ```bash
   curl http://localhost:8080
   ```

### Deployment Failed

1. **Check GitHub Actions logs**:

   - Go to Actions tab
   - Click on failed workflow
   - Review error messages

2. **Verify secrets are set**:

   - Settings → Secrets → Actions
   - Ensure all 3 secrets exist

3. **Test SSH connection**:
   ```bash
   ssh -i /path/to/ShadIn.pem ubuntu@13.60.157.187
   ```

---

## Useful Commands

### Docker Commands

```bash
# Start all services
docker compose up -d

# Stop all services
docker compose down

# Restart all services
docker compose restart

# Rebuild specific service
docker compose up -d --build web

# View container stats
docker stats

# Remove unused images
docker image prune -f

# Remove all stopped containers
docker container prune -f

# View disk usage
docker system df

# Clean up everything (⚠️ destroys data)
docker compose down -v
```

### Django Management Commands

```bash
# Run migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

# Collect static files
docker compose exec web python manage.py collectstatic --noinput

# Open Django shell
docker compose exec web python manage.py shell

# Run custom management command
docker compose exec web python manage.py <command>
```

### Database Commands

```bash
# Access PostgreSQL shell
docker compose exec db psql -U postgres -d jotit

# Backup database
docker compose exec db pg_dump -U postgres jotit > backup_$(date +%Y%m%d).sql

# Restore database
cat backup.sql | docker compose exec -T db psql -U postgres -d jotit

# List databases
docker compose exec db psql -U postgres -c "\l"

# List tables
docker compose exec db psql -U postgres -d jotit -c "\dt"
```

### Server Monitoring

```bash
# Check disk space
df -h

# Check memory usage
free -h

# Check CPU usage
top

# Check running processes
ps aux | grep python

# Check network connections
netstat -tuln | grep 8080

# View system logs
journalctl -xe
```

### Git Commands

```bash
# Check current branch
git branch --show-current

# View recent commits
git log --oneline -10

# View file changes
git status

# Discard local changes
git reset --hard

# Pull latest changes
git pull origin dev

# Switch branches
git checkout dev
```

---

## Access Points

After successful deployment, access your application at:

- **Main Application**: http://13.60.157.187:8080
- **Django Admin**: http://13.60.157.187:8080/admin
- **PgAdmin**: http://13.60.157.187:5050
  - Email: `admin@local.com`
  - Password: `admin`

---

## Security Recommendations

### Production Checklist

- [ ] Change `DEBUG=False` in production
- [ ] Use strong `SECRET_KEY`
- [ ] Use strong database passwords
- [ ] Restrict `ALLOWED_HOSTS` to your domain
- [ ] Set up HTTPS with SSL certificate
- [ ] Use environment-specific settings
- [ ] Enable firewall (UFW)
- [ ] Regular security updates
- [ ] Database backups
- [ ] Monitor logs

### SSL/HTTPS Setup

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Install Nginx
sudo apt install nginx

# Configure Nginx (see DEPLOYMENT.md for full config)

# Get SSL certificate
sudo certbot --nginx -d your-domain.com
```

---

## Backup Strategy

### Database Backup

```bash
# Create backup script
cat > ~/backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cd ~/ShardIn
docker compose exec -T db pg_dump -U postgres jotit > ~/backups/db_backup_$DATE.sql
# Keep only last 7 days
find ~/backups -name "db_backup_*.sql" -mtime +7 -delete
EOF

chmod +x ~/backup.sh

# Add to crontab (daily at 2 AM)
crontab -e
# Add line: 0 2 * * * /home/ubuntu/backup.sh
```

### Code Backup

Your code is automatically backed up in GitHub!

---

## Support

For issues or questions:

1. Check this documentation
2. Review GitHub Actions logs
3. Check container logs: `docker compose logs`
4. Review AWS EC2 console
5. Check security group settings

---

## Quick Reference

### Most Common Commands

```bash
# Deploy changes
git add . && git commit -m "message" && git push origin dev

# Check deployment status
docker compose ps

# View logs
docker compose logs -f web

# Restart application
docker compose restart web

# Run migrations
docker compose exec web python manage.py migrate

# Access server
ssh -i /path/to/ShadIn.pem ubuntu@13.60.157.187
```

---

**Last Updated**: December 23, 2025  
**Version**: 1.0  
**Maintainer**: Hanzala
