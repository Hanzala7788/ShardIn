# GitHub Secrets Setup Guide

## 🔴 Current Issue

Your workflow is failing with "Error: missing server host" because the GitHub secrets are not configured yet.

## ✅ Required Secrets

You need to add 3 secrets to your GitHub repository:

### 1. AWS_HOST

**What it is:** Your EC2 instance's public IP address or DNS name

**How to find it:**

- Go to AWS Console → EC2 → Instances
- Select your instance
- Look for "Public IPv4 address" or "Public IPv4 DNS"

**Example values:**

```
54.123.45.67
```

or

```
ec2-54-123-45-67.compute-1.amazonaws.com
```

### 2. AWS_USER

**What it is:** The username you use to SSH into your EC2 instance

**Value:** `ubuntu` (for Ubuntu AMI)

### 3. AWS_SSH_KEY

**What it is:** Your private SSH key content (the ShadIn.pem file)

**How to get it:**

```bash
# Find your PEM file
find ~ -name "ShadIn.pem" -o -name "*.pem" 2>/dev/null

# Display its content
cat ~/path/to/ShadIn.pem
```

**What to copy:** The entire content including:

```
-----BEGIN RSA PRIVATE KEY-----
[all the lines]
-----END RSA PRIVATE KEY-----
```

## 📝 How to Add Secrets to GitHub

### Step-by-Step Instructions:

1. **Go to your repository on GitHub:**

   ```
   https://github.com/Hanzala7788/ShardIn
   ```

2. **Navigate to Settings:**

   - Click on "Settings" tab (top right)
   - In the left sidebar, click "Secrets and variables"
   - Click "Actions"

3. **Add each secret:**

   **For AWS_HOST:**

   - Click "New repository secret"
   - Name: `AWS_HOST`
   - Secret: Your EC2 IP address
   - Click "Add secret"

   **For AWS_USER:**

   - Click "New repository secret"
   - Name: `AWS_USER`
   - Secret: `ubuntu`
   - Click "Add secret"

   **For AWS_SSH_KEY:**

   - Click "New repository secret"
   - Name: `AWS_SSH_KEY`
   - Secret: Paste the entire content of your PEM file
   - Click "Add secret"

## 🧪 Testing After Adding Secrets

Once you've added all three secrets:

1. Go to "Actions" tab in your repository
2. Click on "Deploy to Amazon Ubuntu VM" workflow
3. Click "Run workflow" button
4. Select "dev" branch
5. Click "Run workflow"

The debug step will now show:

```
✓ AWS_HOST is set: true
✓ AWS_USER is set: true
✓ AWS_SSH_KEY is set: true
✓ All required secrets are configured ✓
```

## 🔍 Finding Your PEM File

If you can't find your `ShadIn.pem` file, try these commands:

```bash
# Search entire home directory
find ~ -name "*.pem" -type f 2>/dev/null

# Common locations
ls ~/Downloads/*.pem
ls ~/.ssh/*.pem
ls ~/Desktop/*.pem
```

## 📋 Checklist

- [ ] Found EC2 instance public IP/DNS
- [ ] Located ShadIn.pem file
- [ ] Added AWS_HOST secret to GitHub
- [ ] Added AWS_USER secret to GitHub
- [ ] Added AWS_SSH_KEY secret to GitHub
- [ ] Tested workflow run

## ⚠️ Security Notes

1. **Never commit your PEM file to Git**
2. **Never share your private key publicly**
3. **GitHub secrets are encrypted and only visible during workflow runs**
4. **The debug step only shows if secrets exist, not their actual values**

## 🆘 Still Having Issues?

If the workflow still fails after adding secrets:

1. **Verify secrets are added:**

   - Go to Settings → Secrets and variables → Actions
   - You should see all three secrets listed

2. **Check the debug step output:**

   - It will tell you which secret is missing

3. **Verify your EC2 instance:**
   - Make sure it's running
   - Check security group allows SSH (port 22)
   - Try SSH manually: `ssh -i ShadIn.pem ubuntu@your-ec2-ip`

## 📞 Need Help?

Common issues:

- **"Permission denied"**: Wrong SSH key or username
- **"Connection timeout"**: Security group doesn't allow SSH from GitHub IPs
- **"Host key verification failed"**: First-time connection, will auto-resolve
