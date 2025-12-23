#!/bin/bash

# Script to create a Django superuser for the admin panel
# Usage: ./create_superuser.sh [email] [password]

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Django Superuser Creation Script ===${NC}\n"

# Check if we're in the correct directory
if [ ! -f "manage.py" ]; then
    echo -e "${RED}Error: manage.py not found. Please run this script from the project root.${NC}"
    exit 1
fi

# Detect if running in Docker environment
DOCKER_CONTAINER="jotit_web"
USE_DOCKER=false

# Check if docker-compose is available and container is running
if command -v docker &> /dev/null; then
    if docker ps --format '{{.Names}}' | grep -q "^${DOCKER_CONTAINER}$"; then
        USE_DOCKER=true
        echo -e "${BLUE}ℹ Detected Docker container: ${DOCKER_CONTAINER}${NC}"
        echo -e "${BLUE}ℹ Commands will be executed inside the container${NC}\n"
    fi
fi

# Prepare the command based on environment
if [ "$USE_DOCKER" = true ]; then
    CMD_PREFIX="docker exec -it ${DOCKER_CONTAINER}"
else
    CMD_PREFIX=""
fi

# Check if arguments are provided
if [ $# -eq 2 ]; then
    # Non-interactive mode with email and password provided
    EMAIL=$1
    PASSWORD=$2
    echo -e "${YELLOW}Creating superuser with email: ${EMAIL}${NC}"
    
    if [ "$USE_DOCKER" = true ]; then
        docker exec ${DOCKER_CONTAINER} python manage.py createsuperuser --email "$EMAIL" --password "$PASSWORD"
    else
        python manage.py createsuperuser --email "$EMAIL" --password "$PASSWORD"
    fi
elif [ $# -eq 0 ]; then
    # Interactive mode
    echo -e "${YELLOW}Running in interactive mode...${NC}\n"
    
    if [ "$USE_DOCKER" = true ]; then
        docker exec -it ${DOCKER_CONTAINER} python manage.py createsuperuser
    else
        python manage.py createsuperuser
    fi
else
    echo -e "${RED}Error: Invalid number of arguments.${NC}"
    echo -e "${YELLOW}Usage:${NC}"
    echo -e "  Interactive mode:     ./create_superuser.sh"
    echo -e "  Non-interactive mode: ./create_superuser.sh <email> <password>"
    echo ""
    echo -e "${YELLOW}Alternative - Direct Docker commands:${NC}"
    echo -e "  Interactive:          docker exec -it ${DOCKER_CONTAINER} python manage.py createsuperuser"
    echo -e "  Non-interactive:      docker exec ${DOCKER_CONTAINER} python manage.py createsuperuser --email <email> --password <password>"
    exit 1
fi

# Check if the command was successful
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✓ Superuser created successfully!${NC}"
    echo -e "${YELLOW}You can now log in to the admin panel at: http://your-domain/admin/${NC}"
else
    echo -e "\n${RED}✗ Failed to create superuser.${NC}"
    exit 1
fi
