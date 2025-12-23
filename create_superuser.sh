#!/bin/bash

# Script to create a Django superuser for the admin panel
# Usage: ./create_superuser.sh [email] [password]

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Django Superuser Creation Script ===${NC}\n"

# Check if we're in the correct directory
if [ ! -f "manage.py" ]; then
    echo -e "${RED}Error: manage.py not found. Please run this script from the project root.${NC}"
    exit 1
fi

# Check if arguments are provided
if [ $# -eq 2 ]; then
    # Non-interactive mode with email and password provided
    EMAIL=$1
    PASSWORD=$2
    echo -e "${YELLOW}Creating superuser with email: ${EMAIL}${NC}"
    python manage.py createsuperuser --email "$EMAIL" --password "$PASSWORD"
elif [ $# -eq 0 ]; then
    # Interactive mode
    echo -e "${YELLOW}Running in interactive mode...${NC}\n"
    python manage.py createsuperuser
else
    echo -e "${RED}Error: Invalid number of arguments.${NC}"
    echo -e "${YELLOW}Usage:${NC}"
    echo -e "  Interactive mode:     ./create_superuser.sh"
    echo -e "  Non-interactive mode: ./create_superuser.sh <email> <password>"
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
