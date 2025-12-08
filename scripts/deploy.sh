#!/bin/bash
#
# Fusion Beef - Deploy Script
# Automated deployment to Digital Ocean droplet
#

set -e  # Exit on error

# Configuration
DROPLET_IP="159.65.167.133"
DROPLET_USER="root"
GITHUB_REPO="https://github.com/smartfusionoficial/FUSION-BEEF.git"
APP_DIR="/var/www/fusion-beef"
APP_NAME="fusion-beef"

echo "========================================="
echo "Fusion Beef - Automated Deploy"
echo "========================================="
echo ""
echo "Target: $DROPLET_USER@$DROPLET_IP"
echo "Repository: $GITHUB_REPO"
echo ""

# Build the application locally
echo "📦 Building application..."
cd "$(dirname "$0")/.."
pnpm install
pnpm run build

echo "✅ Build completed"
echo ""

# Create deployment package
echo "📦 Creating deployment package..."
tar -czf /tmp/fusion-beef-deploy.tar.gz \
    --exclude='node_modules' \
    --exclude='.git' \
    --exclude='.manus' \
    --exclude='*.log' \
    --exclude='.deploy_token' \
    .

echo "✅ Package created: /tmp/fusion-beef-deploy.tar.gz"
echo ""

# Note: SSH deployment requires SSH key setup
echo "⚠️  SSH Deployment Note:"
echo "This script requires SSH key authentication to be set up."
echo "Please ensure you have added your SSH public key to the droplet."
echo ""
echo "To complete the deployment manually:"
echo ""
echo "1. Copy the package to the server:"
echo "   scp /tmp/fusion-beef-deploy.tar.gz $DROPLET_USER@$DROPLET_IP:/tmp/"
echo ""
echo "2. SSH into the server:"
echo "   ssh $DROPLET_USER@$DROPLET_IP"
echo ""
echo "3. Extract and deploy:"
echo "   mkdir -p $APP_DIR"
echo "   tar -xzf /tmp/fusion-beef-deploy.tar.gz -C $APP_DIR"
echo "   cd $APP_DIR"
echo "   pnpm install --prod"
echo "   pm2 restart $APP_NAME || pm2 start server/index.ts --name $APP_NAME"
echo ""
echo "4. Configure environment variables:"
echo "   nano $APP_DIR/.env"
echo ""
echo "5. Setup cron job for scraper:"
echo "   crontab -e"
echo "   # Add: 0 */2 * * * $APP_DIR/scripts/run_scraper_cron.sh"
echo ""
echo "========================================="
echo "Package ready for deployment!"
echo "Location: /tmp/fusion-beef-deploy.tar.gz"
echo "========================================="
