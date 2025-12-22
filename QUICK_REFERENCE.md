# ShardIn - Quick Deployment Reference

## 🚀 Quick Setup on AWS Ubuntu VM

### One-Time Setup

```bash
# 1. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
sudo apt install docker-compose-plugin -y

# 2. Clone repository
git clone https://github.com/Hanzala7788/ShardIn.git
cd ShardIn

# 3. Configure environment
cp .env.example .env
nano .env  # Edit with your settings

# 4. Start application
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py collectstatic --noinput
```

## 🔄 Common Commands

### Start/Stop Services

```bash
docker compose up -d          # Start in background
docker compose down           # Stop all services
docker compose restart        # Restart all services
```

### View Logs

```bash
docker compose logs -f web    # Follow web logs
docker compose logs db        # View database logs
docker compose ps             # Check container status
```

### Run Django Commands

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py collectstatic --noinput
docker compose exec web python manage.py shell
```

### Access Containers

```bash
docker compose exec web bash                    # Web container shell
docker compose exec db psql -U postgres -d jotit  # Database shell
```

## 🔧 GitHub Actions Deployment

### Required Secrets

Add in GitHub: `Settings` → `Secrets and variables` → `Actions`

| Secret        | Value                |
| ------------- | -------------------- |
| `AWS_HOST`    | Your EC2 IP/domain   |
| `AWS_USER`    | `ubuntu`             |
| `AWS_SSH_KEY` | Your private SSH key |
| `AWS_PORT`    | `22` (optional)      |

### Workflow Trigger

- Automatic: Push to `main` or `production` branch
- Manual: GitHub Actions tab → "Run workflow"

## 🌐 Access Points

- **Application**: http://your-ip:8080
- **PgAdmin**: http://your-ip:5050
- **Database**: localhost:5432 (from server)

## 📊 Monitoring

```bash
# Container stats
docker stats

# Disk usage
docker system df

# Clean up unused resources
docker system prune -f
```

## 🆘 Troubleshooting

### Application not starting?

```bash
docker compose logs web
docker compose restart web
```

### Database connection issues?

```bash
docker compose logs db
docker compose restart db
```

### Reset everything (⚠️ destroys data)

```bash
docker compose down -v
docker compose up -d --build
```
