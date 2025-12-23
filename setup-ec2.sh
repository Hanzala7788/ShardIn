#!/bin/bash

# ShardIn EC2 Server Setup Script
# Run this script on your EC2 instance to prepare it for deployment

set -e  # Exit on error

echo "=========================================="
echo "ShardIn EC2 Server Setup"
echo "=========================================="

# Update system packages
echo ""
echo "Step 1: Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Docker
echo ""
echo "Step 2: Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    rm get-docker.sh
    
    # Add current user to docker group
    sudo usermod -aG docker $USER
    echo "✓ Docker installed successfully"
else
    echo "✓ Docker is already installed"
fi

# Install Docker Compose plugin
echo ""
echo "Step 3: Installing Docker Compose..."
if ! docker compose version &> /dev/null; then
    sudo apt install -y docker-compose-plugin
    echo "✓ Docker Compose installed successfully"
else
    echo "✓ Docker Compose is already installed"
fi

# Install Git
echo ""
echo "Step 4: Installing Git..."
if ! command -v git &> /dev/null; then
    sudo apt install -y git
    echo "✓ Git installed successfully"
else
    echo "✓ Git is already installed"
fi

# Clone repository
echo ""
echo "Step 5: Cloning ShardIn repository..."
if [ ! -d "$HOME/ShardIn" ]; then
    cd ~
    git clone https://github.com/Hanzala7788/ShardIn.git
    cd ShardIn
    echo "✓ Repository cloned successfully"
else
    echo "✓ Repository already exists"
    cd ~/ShardIn
    git pull origin main
    echo "✓ Repository updated"
fi

# Create .env file
echo ""
echo "Step 6: Setting up environment file..."
if [ ! -f "$HOME/ShardIn/.env" ]; then
    if [ -f "$HOME/ShardIn/.env.example" ]; then
        cp $HOME/ShardIn/.env.example $HOME/ShardIn/.env
        echo "✓ Created .env file from .env.example"
        echo ""
        echo "⚠️  IMPORTANT: You need to edit the .env file with your settings:"
        echo "   nano ~/ShardIn/.env"
    else
        echo "⚠️  .env.example not found. You'll need to create .env manually"
    fi
else
    echo "✓ .env file already exists"
fi

# Start Docker service
echo ""
echo "Step 7: Starting Docker service..."
sudo systemctl start docker
sudo systemctl enable docker
echo "✓ Docker service started and enabled"

# Display versions
echo ""
echo "=========================================="
echo "Installation Summary"
echo "=========================================="
docker --version
docker compose version
git --version

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Log out and log back in for Docker group changes to take effect:"
echo "   exit"
echo "   ssh -i ShadIn.pem ubuntu@13.60.157.187"
echo ""
echo "2. Edit the .env file with your configuration:"
echo "   nano ~/ShardIn/.env"
echo ""
echo "3. Start the application:"
echo "   cd ~/ShardIn"
echo "   docker compose up -d --build"
echo "   docker compose exec web python manage.py migrate"
echo "   docker compose exec web python manage.py createsuperuser"
echo "   docker compose exec web python manage.py collectstatic --noinput"
echo ""
echo "4. After that, GitHub Actions will handle future deployments automatically!"
echo ""
