# ShardIn

A Django-based social media automation platform for scheduling and publishing LinkedIn posts with OAuth integration.

## 🚀 Features

- **LinkedIn Integration**: OAuth authentication with LinkedIn for seamless post publishing
- **Post Scheduling**: Schedule posts to be published at specific times or share immediately
- **User Management**: Custom user model with email-based authentication
- **REST API**: Full-featured REST API built with Django REST Framework
- **JWT Authentication**: Secure API authentication using SimpleJWT
- **Admin Panel**: Django admin interface for managing users and posts
- **Docker Support**: Fully containerized application with Docker Compose
- **PostgreSQL Database**: Production-ready database setup
- **LinkedIn Job Scraper**: Automated job scraping functionality for LinkedIn

## 📋 Prerequisites

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 15 (if running without Docker)
- LinkedIn Developer Account (for OAuth integration)

## 🛠️ Tech Stack

- **Backend**: Django 5.2.0
- **API**: Django REST Framework 3.16.0
- **Database**: PostgreSQL 15
- **Authentication**: JWT (djangorestframework-simplejwt), django-allauth
- **Server**: Gunicorn
- **Containerization**: Docker & Docker Compose
- **Static Files**: WhiteNoise

## 📦 Installation

### Option 1: Docker (Recommended)

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd ShardIn
   ```

2. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Build and run with Docker Compose**

   ```bash
   docker-compose up -d --build
   ```

4. **Create a superuser**

   ```bash
   docker exec -it jotit_web python manage.py createsuperuser
   ```

5. **Access the application**
   - API: http://localhost:8080
   - Admin Panel: http://localhost:8080/admin
   - PgAdmin: http://localhost:5050

### Option 2: Local Development

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd ShardIn
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Django Settings
PRODUCTION=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=["localhost", "127.0.0.1", "0.0.0.0"]

# API Configuration
API_HOST=http://127.0.0.1:8000

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ShadIn
DB_USER=postgres
DB_PASSWORD=your-password

# OAuth Settings
OAUTHLIB_INSECURE_TRANSPORT=1  # Set to 0 in production

# CORS (Optional)
# CORS_ALLOWED_ORIGINS=["http://127.0.0.1:9000"]
# FRONTEND_HOST=http://localhost:4200
```

### LinkedIn OAuth Setup

1. Create a LinkedIn App at [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Configure OAuth redirect URLs
3. Add credentials to your Django admin under Social Applications
4. Enable the following LinkedIn API scopes:
   - `r_liteprofile`
   - `w_member_social`

## 📚 API Endpoints

### Authentication

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login (JWT)
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Posts

- `GET /api/posts/` - List all posts
- `POST /api/posts/` - Create a new post
- `GET /api/posts/{id}/` - Get post details
- `PUT /api/posts/{id}/` - Update a post
- `DELETE /api/posts/{id}/` - Delete a post

### Users

- `GET /api/users/me/` - Get current user profile
- `PUT /api/users/me/` - Update user profile

## 🐳 Docker Services

The application includes three Docker services:

1. **web** (`jotit_web`): Django application running on port 8080
2. **db** (`jotit_db`): PostgreSQL database on port 5432
3. **pgadmin** (`jotit_pgadmin`): Database management tool on port 5050

### Useful Docker Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f web

# Execute commands in container
docker exec -it jotit_web python manage.py <command>

# Rebuild containers
docker-compose up -d --build

# Access Django shell
docker exec -it jotit_web python manage.py shell
```

## 🔧 Management Commands

### Create Superuser

```bash
# Interactive mode
./create_superuser.sh

# Non-interactive mode
./create_superuser.sh admin@example.com SecurePassword123

# Docker environment
docker exec -it jotit_web python manage.py createsuperuser
```

See [CREATE_SUPERUSER_GUIDE.md](CREATE_SUPERUSER_GUIDE.md) for detailed instructions.

## 📝 Project Structure

```
ShardIn/
├── apps/
│   ├── posts/          # Post management app
│   ├── users/          # Custom user model and authentication
│   └── __init__.py
├── config/
│   ├── settings/       # Django settings (dev, prod)
│   ├── urls.py         # URL configuration
│   └── wsgi.py         # WSGI configuration
├── helper/
│   └── linkedin.py     # LinkedIn API integration
├── staticfiles/        # Collected static files
├── .env.example        # Environment variables template
├── docker-compose.yaml # Docker Compose configuration
├── Dockerfile          # Docker image definition
├── entrypoint.sh       # Container entrypoint script
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## 🚀 Deployment

### AWS EC2 Deployment

1. **SSH into your EC2 instance**

   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

2. **Clone and setup**

   ```bash
   git clone <repository-url>
   cd ShardIn
   ```

3. **Configure environment**

   ```bash
   cp .env.example .env
   # Edit .env with production settings
   ```

4. **Deploy with Docker**

   ```bash
   docker-compose up -d --build
   ```

5. **Create superuser**
   ```bash
   docker exec -it jotit_web python manage.py createsuperuser
   ```

See [DEPLOY.md](DEPLOY.md) for detailed deployment instructions.

## 🧪 Development

### Running Tests

```bash
python manage.py test
```

### Jupyter Notebook Support

The project includes Jupyter support for data analysis and experimentation:

```bash
python manage.py shell_plus --notebook
```

### Database Migrations

```bash
# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations
```

## 🔐 Security

- JWT tokens for API authentication
- CORS protection with django-cors-headers
- Environment-based configuration
- PostgreSQL with secure credentials
- OAuth 2.0 for LinkedIn integration

**Production Checklist:**

- [ ] Set `PRODUCTION=True` in `.env`
- [ ] Use strong `SECRET_KEY`
- [ ] Set `OAUTHLIB_INSECURE_TRANSPORT=0`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Use HTTPS for all endpoints
- [ ] Enable database backups
- [ ] Set up monitoring and logging

## 📖 Additional Documentation

- [CREATE_SUPERUSER_GUIDE.md](CREATE_SUPERUSER_GUIDE.md) - Superuser creation guide
- [DEPLOY.md](DEPLOY.md) - Deployment instructions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'django'`

- **Solution**: Make sure you're running commands inside the Docker container or have activated your virtual environment

**Issue**: Database connection errors

- **Solution**: Ensure PostgreSQL is running and credentials in `.env` are correct

**Issue**: LinkedIn OAuth not working

- **Solution**: Check that redirect URLs are properly configured in LinkedIn Developer Console

**Issue**: Static files not loading

- **Solution**: Run `python manage.py collectstatic`

### Getting Help

For more help, check:

- Django documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- LinkedIn API: https://docs.microsoft.com/en-us/linkedin/

## 👥 Authors

- **Hanzala** - Initial work

## 🙏 Acknowledgments

- Django community
- Django REST Framework
- LinkedIn API documentation
