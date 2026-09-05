# Production Deployment Guide (Single-Node Architecture)

This guide documents the steps required to deploy the Customer Churn Analysis & Prediction platform onto a single Linux virtual machine (e.g., AWS EC2, DigitalOcean Droplet, Linode) using Docker Compose.

## Prerequisites
1. A Linux Virtual Machine (Ubuntu 22.04 LTS recommended) with at least 2GB RAM.
2. A domain name (or subdomain) pointing to your VM's public IP address (e.g., `churn.yourdomain.com`).
3. SSH access to the VM.

## Step 1: Server Provisioning & Setup

SSH into your new server and install Docker and Docker Compose:

```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to the docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose-plugin -y
```

Log out and log back in for the group changes to take effect.

## Step 2: Clone the Repository

Clone your project to the server:

```bash
git clone https://github.com/yourusername/customer-churn-platform.git
cd customer-churn-platform
```

## Step 3: Configure Environment Variables

Create the `.env` file in the root directory. **Never commit this file to GitHub.**

```bash
nano .env
```

Add the following production configuration:

```ini
# Database Configuration
POSTGRES_USER=churnadmin
POSTGRES_PASSWORD=your_super_secure_password_here
POSTGRES_DB=churn_prod_db

# Frontend Configuration (Used by Docker Compose during build)
# Replace with your actual domain name
VITE_API_URL=https://api.churn.yourdomain.com

# Backend Configuration
FRONTEND_URL=https://churn.yourdomain.com
```

## Step 4: Configure the Reverse Proxy & SSL (Nginx + Certbot)

For a production deployment, we need HTTPS. We will use Nginx on the host machine to route traffic to our Docker containers and Certbot to automatically provision Let's Encrypt SSL certificates.

Install Nginx and Certbot:
```bash
sudo apt install nginx certbot python3-certbot-nginx -y
```

Create an Nginx configuration file:
```bash
sudo nano /etc/nginx/sites-available/churn-platform
```

Add the following configuration (replace the domain names):
```nginx
server {
    listen 80;
    server_name churn.yourdomain.com;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 80;
    server_name api.churn.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/churn-platform /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

Provision SSL Certificates:
```bash
sudo certbot --nginx -d churn.yourdomain.com -d api.churn.yourdomain.com
```

## Step 5: Build and Run the Containers

With the environment configured and the reverse proxy routing traffic, build and start the Docker containers:

```bash
docker compose build --build-arg VITE_API_URL=$VITE_API_URL
docker compose up -d
```

## Step 6: Verify Deployment

1. **Frontend**: Navigate to `https://churn.yourdomain.com`. You should see the React dashboard load over HTTPS.
2. **API Health**: Navigate to `https://api.churn.yourdomain.com/health`. You should see `{"status": "healthy", "version": "1.0.0"}`.
3. **Database**: The PostgreSQL database is mapped to a local Docker volume, ensuring data persistence across container restarts.

## Maintenance

To view logs:
```bash
docker compose logs -f
```

To update the application after pushing new code:
```bash
git pull
docker compose build
docker compose up -d
```
