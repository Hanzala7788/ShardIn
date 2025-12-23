# Django Superuser Creation Guide

This guide explains how to create a superuser for your Django admin panel when running in Docker.

## 🐳 Docker Environment (EC2 Instance)

Since your application runs in Docker containers, you need to execute the Django management command **inside** the container.

### Method 1: Using the Shell Script (Recommended)

The `create_superuser.sh` script automatically detects if you're running in Docker and executes the command in the correct environment.

#### Interactive Mode (prompts for credentials):

```bash
cd ~/ShardIn
./create_superuser.sh
```

#### Non-Interactive Mode (provide credentials directly):

```bash
./create_superuser.sh admin@example.com YourSecurePassword123
```

### Method 2: Direct Docker Commands

#### Interactive Mode:

```bash
docker exec -it jotit_web python manage.py createsuperuser
```

This will prompt you for:

- Email address
- Password (hidden input)
- Password confirmation

#### Non-Interactive Mode:

```bash
docker exec jotit_web python manage.py createsuperuser --email admin@example.com --password YourSecurePassword123
```

#### With Optional First/Last Name:

```bash
docker exec jotit_web python manage.py createsuperuser \
  --email admin@example.com \
  --password YourSecurePassword123 \
  --first_name John \
  --last_name Doe
```

## 📋 Quick Commands for EC2

```bash
# 1. SSH into your EC2 instance
ssh -i /path/to/your-key.pem ubuntu@your-ec2-ip

# 2. Navigate to project directory
cd ~/ShardIn

# 3. Check if containers are running
docker ps

# 4. Create superuser (interactive)
docker exec -it jotit_web python manage.py createsuperuser

# 5. Access admin panel
# Open browser: http://your-ec2-ip:8080/admin/
```

## 🔍 Troubleshooting

### Container Not Running

If you get an error that the container doesn't exist:

```bash
# Check running containers
docker ps

# If not running, start them
docker-compose up -d

# Wait a few seconds, then try again
docker exec -it jotit_web python manage.py createsuperuser
```

### Permission Denied

If you get permission errors:

```bash
# Make the script executable
chmod +x create_superuser.sh

# Then run it
./create_superuser.sh
```

### User Already Exists

If you get an error that the user already exists, you can either:

1. Use a different email address
2. Delete the existing user from the database
3. Use Django's password reset functionality

## 🎯 Example Session

```bash
ubuntu@ip-172-31-46-29:~/ShardIn$ docker exec -it jotit_web python manage.py createsuperuser
Email address: admin@shardin.com
Password:
Password (again):
Superuser admin@shardin.com created successfully!
```

## 🌐 Accessing the Admin Panel

After creating the superuser:

1. Open your browser
2. Navigate to: `http://your-ec2-ip:8080/admin/`
3. Log in with the email and password you just created

## 📝 Notes

- The container name is `jotit_web` (defined in docker-compose.yaml)
- The Django app runs on port 8000 inside the container, mapped to port 8080 on the host
- Passwords are not shown when typing (for security)
- Email addresses must be unique
