# EC2 Server Setup Guide

## 🚀 Quick Setup (Automated)

### Step 1: Copy Setup Script to EC2

From your local machine, run:

```bash
# Copy the setup script to your EC2 instance
scp -i /home/hanzala/ShadIn.pem setup-ec2.sh ubuntu@13.60.157.187:~/

# SSH into your EC2 instance
ssh -i /home/hanzala/ShadIn.pem ubuntu@13.60.157.187
```

### Step 2: Run the Setup Script

Once connected to your EC2 instance:

```bash
# Make the script executable
chmod +x setup-ec2.sh

# Run the setup script
./setup-ec2.sh
```

The script will automatically:

- ✅ Update system packages
- ✅ Install Docker
- ✅ Install Docker Compose
- ✅ Install Git
- ✅ Clone your ShardIn repository
- ✅ Create .env file from template

### Step 3: Log Out and Back In

After the script completes, log out and back in for Docker permissions to take effect:

```bash
exit
ssh -i /home/hanzala/ShadIn.pem ubuntu@13.60.157.187
```

### Step 4: Configure Environment Variables

Edit the `.env` file with your settings:

```bash
cd ~/ShardIn
nano .env
```

Update these values:

```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=13.60.157.187,your-domain.com

# Database settings (match docker-compose.yaml)
DB_NAME=jotit
DB_USER=postgres
DB_USER_PASSWORD=your_secure_password
DATABASE_HOST=db
DATABASE_PORT=5432
```

Save and exit (Ctrl+X, then Y, then Enter)

### Step 5: Start the Application

```bash
cd ~/ShardIn

# Build and start all services
docker compose up -d --build

# Wait for services to start
sleep 10

# Run migrations
docker compose exec web python manage.py migrate

# Create superuser (interactive)
docker compose exec web python manage.py createsuperuser

# Collect static files
docker compose exec web python manage.py collectstatic --noinput

# Check status
docker compose ps
```

### Step 6: Verify Deployment

```bash
# Check if containers are running
docker compose ps

# View logs
docker compose logs web

# Test the application
curl http://localhost:8080
```

### Step 7: Configure Security Group (AWS Console)

Make sure your EC2 security group allows:

| Type       | Protocol | Port | Source    | Description                |
| ---------- | -------- | ---- | --------- | -------------------------- |
| SSH        | TCP      | 22   | Your IP   | For SSH access             |
| HTTP       | TCP      | 80   | 0.0.0.0/0 | For web traffic            |
| HTTPS      | TCP      | 443  | 0.0.0.0/0 | For secure web traffic     |
| Custom TCP | TCP      | 8080 | 0.0.0.0/0 | For Django app (temporary) |

---

## 🔧 Manual Setup (Alternative)

If you prefer to set up manually:

### 1. Install Docker

```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo apt install docker-compose-plugin -y

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker
```

### 2. Install Git

```bash
sudo apt install git -y
```

### 3. Clone Repository

```bash
cd ~
git clone https://github.com/Hanzala7788/ShardIn.git
cd ShardIn
```

### 4. Configure Environment

```bash
cp .env.example .env
nano .env
```

### 5. Start Application

```bash
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py collectstatic --noinput
```

---

## 🎯 After Setup

Once the server is set up, GitHub Actions will automatically deploy when you push to the `dev` or `production` branch!

### Test GitHub Actions Deployment

1. Make a small change to your code
2. Commit and push to `dev` branch:
   ```bash
   git add .
   git commit -m "Test deployment"
   git push origin dev
   ```
3. Watch the deployment in GitHub Actions tab

---

## 🆘 Troubleshooting

### Docker permission denied

```bash
# Add user to docker group
sudo usermod -aG docker ubuntu

# Log out and back in
exit
ssh -i /home/hanzala/ShadIn.pem ubuntu@13.60.157.187
```

### Port 8080 already in use

```bash
# Stop existing containers
docker compose down

# Check what's using the port
sudo lsof -i :8080

# Restart
docker compose up -d
```

### Database connection errors

```bash
# Check database container
docker compose logs db

# Restart database
docker compose restart db
```

### Application not starting

```bash
# View logs
docker compose logs web

# Restart web container
docker compose restart web
```

---

## 📊 Useful Commands

```bash
# View all containers
docker compose ps

# View logs
docker compose logs -f web

# Restart services
docker compose restart

# Stop all services
docker compose down

# Rebuild and restart
docker compose up -d --build

# Access web container shell
docker compose exec web bash

# Access database
docker compose exec db psql -U postgres -d jotit
```

---

## 🌐 Access Your Application

- **Application**: http://13.60.157.187:8080
- **Admin Panel**: http://13.60.157.187:8080/admin
- **PgAdmin**: http://13.60.157.187:5050

---

## 🔒 Optional: Set Up Nginx Reverse Proxy

For production, set up Nginx:

```bash
# Install Nginx
sudo apt install nginx -y

# Create configuration
sudo nano /etc/nginx/sites-available/shardin
```

Add this configuration:

```nginx
server {
    listen 80;
    server_name 13.60.157.187;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable and restart:

```bash
sudo ln -s /etc/nginx/sites-available/shardin /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

Now access via: http://13.60.157.187
