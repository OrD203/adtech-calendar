#!/bin/bash

# AdTech Calendar Auto-Update Setup Script
# Run this to set up automated daily updates

echo "================================================"
echo "   AdTech Event Calendar - Auto-Update Setup"
echo "================================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Ask user for deployment method
echo "Choose deployment method:"
echo "1) GitHub Actions (FREE, recommended)"
echo "2) Local server with cron"
echo "3) Docker container"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "Setting up for GitHub Actions..."
        echo ""
        
        read -p "Enter your GitHub username: " gh_user
        read -p "Enter repository name (e.g., adtech-calendar): " repo_name
        
        # Create directory structure
        mkdir -p .github/workflows
        
        echo ""
        echo "📦 Files ready for GitHub:"
        echo "  - event_updater.py"
        echo "  - core_events.json"
        echo "  - requirements.txt"
        echo "  - .github/workflows/update-calendar.yml"
        echo "  - index.html (your calendar)"
        echo ""
        echo "Next steps:"
        echo "1. Create repo: https://github.com/new"
        echo "2. Run these commands:"
        echo ""
        echo "   git init"
        echo "   git add ."
        echo "   git commit -m 'Initial calendar setup'"
        echo "   git remote add origin https://github.com/$gh_user/$repo_name.git"
        echo "   git push -u origin main"
        echo ""
        echo "3. Enable GitHub Pages in repo Settings > Pages"
        echo "4. Your calendar will be at: https://$gh_user.github.io/$repo_name/"
        echo ""
        echo "✅ Setup complete! Daily updates will run automatically at 3 AM UTC."
        ;;
        
    2)
        echo ""
        echo "Setting up local cron job..."
        
        # Install Python dependencies
        echo "Installing Python dependencies..."
        pip3 install -r requirements.txt
        
        # Get current directory
        SCRIPT_DIR=$(pwd)
        
        # Add to crontab
        echo ""
        echo "Add this line to your crontab (crontab -e):"
        echo ""
        echo "0 3 * * * cd $SCRIPT_DIR && /usr/bin/python3 event_updater.py"
        echo ""
        
        # Test run
        read -p "Run a test update now? (y/n): " test_run
        if [ "$test_run" = "y" ]; then
            RUN_ONCE=true python3 event_updater.py
            echo ""
            if [ -f events.json ]; then
                echo "✅ Test successful! events.json created."
            else
                echo "❌ Test failed. Check event_updater.log for errors."
            fi
        fi
        ;;
        
    3)
        echo ""
        echo "Setting up Docker container..."
        
        # Create Dockerfile
        cat > Dockerfile << 'DOCKER_EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY event_updater.py .
COPY core_events.json .

VOLUME ["/app/data"]

CMD ["python", "event_updater.py"]
DOCKER_EOF

        # Create docker-compose.yml
        cat > docker-compose.yml << 'COMPOSE_EOF'
version: '3'
services:
  calendar-updater:
    build: .
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    environment:
      - TZ=UTC
      - EVENTS_OUTPUT_PATH=/app/data/events.json
COMPOSE_EOF

        echo ""
        echo "Docker files created!"
        echo ""
        echo "To start:"
        echo "  docker-compose up -d"
        echo ""
        echo "To view logs:"
        echo "  docker-compose logs -f"
        echo ""
        echo "events.json will be in ./data/"
        ;;
        
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "================================================"
echo "Setup complete! 🎉"
echo "================================================"
