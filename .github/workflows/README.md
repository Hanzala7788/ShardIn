# GitHub Actions Deployment Workflow

This workflow automatically deploys your ShardIn application to your AWS Ubuntu VM using Docker Compose.

## How It Works

### Trigger Events

- **Push to `main` or `production` branch**: Automatically deploys
- **Manual trigger**: Use "Run workflow" button in GitHub Actions tab

### Deployment Steps

1. **Checkout Code**: Gets the latest code from the repository
2. **SSH to Server**: Connects to your AWS Ubuntu VM
3. **Pull Changes**: Updates the code on the server
4. **Stop Containers**: Gracefully stops running containers
5. **Rebuild**: Builds new Docker images with latest code
6. **Start Services**: Starts all containers (web, db, pgadmin)
7. **Run Migrations**: Applies database schema changes
8. **Collect Static**: Gathers static files for serving
9. **Verify**: Checks that containers are running and app responds

## Required GitHub Secrets

Configure these in: `Repository Settings` → `Secrets and variables` → `Actions` → `New repository secret`

### AWS_HOST

Your EC2 instance public IP or domain name.

**Example:**

```
ec2-54-123-45-67.compute-1.amazonaws.com
```

or

```
54.123.45.67
```

### AWS_USER

SSH username for your Ubuntu instance (usually `ubuntu`).

**Example:**

```
ubuntu
```

### AWS_SSH_KEY

Your private SSH key content (the `.pem` file you downloaded from AWS).

**To get the key:**

```bash
cat ~/path/to/your-key.pem
```

**Format:**

```
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA...
[full key content]
...
-----END RSA PRIVATE KEY-----
```

### AWS_PORT (Optional)

SSH port number. Defaults to 22 if not set.

**Example:**

```
22
```

## Server Prerequisites

Your AWS Ubuntu VM must have:

1. **Docker and Docker Compose installed**

   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker ubuntu
   sudo apt install docker-compose-plugin -y
   ```

2. **Git installed**

   ```bash
   sudo apt install git -y
   ```

3. **Repository cloned**

   ```bash
   cd ~
   git clone https://github.com/Hanzala7788/ShardIn.git
   ```

4. **Environment file configured**
   ```bash
   cd ~/ShardIn
   cp .env.example .env
   nano .env  # Edit with your settings
   ```

## AWS Security Group Settings

Ensure your EC2 security group allows:

| Type       | Protocol | Port | Source                  |
| ---------- | -------- | ---- | ----------------------- |
| SSH        | TCP      | 22   | Your IP or GitHub IPs   |
| HTTP       | TCP      | 80   | 0.0.0.0/0               |
| HTTPS      | TCP      | 443  | 0.0.0.0/0               |
| Custom TCP | TCP      | 8080 | 0.0.0.0/0 (for testing) |

## Testing the Workflow

### Manual Test

1. Go to your repository on GitHub
2. Click on "Actions" tab
3. Select "Deploy to Amazon Ubuntu VM" workflow
4. Click "Run workflow" button
5. Select branch (usually `main`)
6. Click "Run workflow"

### Monitor Deployment

- Watch the workflow run in real-time in the Actions tab
- Check logs for each step
- SSH to your server to verify:
  ```bash
  ssh ubuntu@your-ec2-instance
  cd ~/ShardIn
  docker compose ps
  docker compose logs web
  ```

## Troubleshooting

### Workflow fails at "Deploy with Docker Compose"

**Check SSH connection:**

```bash
ssh ubuntu@your-ec2-instance
```

**Verify secrets are correct:**

- AWS_HOST matches your EC2 instance
- AWS_USER is correct (usually `ubuntu`)
- AWS_SSH_KEY is the complete private key

### Workflow succeeds but app doesn't work

**SSH to server and check:**

```bash
ssh ubuntu@your-ec2-instance
cd ~/ShardIn
docker compose logs web
docker compose ps
```

**Check if containers are running:**

```bash
docker compose ps
```

**Restart if needed:**

```bash
docker compose restart
```

### Permission denied errors

**Ensure user is in docker group:**

```bash
sudo usermod -aG docker ubuntu
# Then logout and login again
```

## Workflow File Location

The workflow is defined in:

```
.github/workflows/deploy.yml
```

## Customization

### Change deployment branch

Edit the workflow file:

```yaml
on:
  push:
    branches:
      - main
      - your-branch-name # Add your branch
```

### Add pre-deployment tests

Add a test job before deployment:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: |
          # Your test commands

  deploy:
    needs: test # Only deploy if tests pass
    # ... rest of deploy job
```

### Change deployment path

If your app is in a different directory on the server, update:

```yaml
script: |
  cd ~/YourDirectory  # Change this line
  git pull origin main
  # ... rest of script
```

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
