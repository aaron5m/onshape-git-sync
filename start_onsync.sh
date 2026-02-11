#!/usr/bin/env bash

# Get the current dir and path to script, and path to docker
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DOCKER_PATH="$(which docker)"

# Make sure scripts can execute
chmod +x "$SCRIPT_DIR/start_onsync.sh"
chmod +x "$SCRIPT_DIR/git_push.sh"

# Check if script is run by cron
if ! command -v crontab &>/dev/null; then
    echo "Cron is not installed. Installing..."
    
    # Detect the package manager and install cron
    if [ -f /etc/debian_version ]; then
        # For Debian/Ubuntu
        sudo apt-get update && sudo apt-get install -y cron
    elif [ -f /etc/redhat-release ]; then
        # For RedHat/CentOS
        sudo yum install -y cronie
    elif [ -f /etc/amazon-release ]; then
        # For Amazon Linux
        sudo yum install -y cronie
    else
        echo "Unsupported OS, cannot install cron."
        exit 1
    fi

    # Start cron service
    sudo service cron start
    echo "Cron installed and started."
else
    echo "Cron is already installed."
fi

# Prepare a cron job that will run every hour
CRON_JOB="0/3 * * * * $DOCKER_PATH run --rm \
 --env-file $SCRIPT_DIR/onsync.env \
 -v $SCRIPT_DIR/logs:/app/logs \
 -v $SCRIPT_DIR/snapshots:/app/snapshots \
 onshape-git-sync && $SCRIPT_DIR/git_push.sh"

# Add that cron job (if it does not already exist)
crontab -l 2>/dev/null | grep -F "$DOCKER_PATH" > /dev/null
if [ $? -ne 0 ]; then
    # Add it if missing
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "Cron job added: $CRON_JOB"
else
    echo "Cron job already exists."
fi

echo "$DOCKER_PATH"

# Build the docker image
"$DOCKER_PATH" build -t onshape-git-sync .


# Run docker
"$DOCKER_PATH" run --rm \
 --env-file onsync.env \
 -v "$(pwd)/logs:/app/logs" \
 -v "$(pwd)/snapshots:/app/snapshots" \
 onshape-git-sync
 
 # Push to git
 bash "$SCRIPT_DIR/git_push.sh"
