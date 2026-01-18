#!/bin/bash
set -e

echo "--- PulseAI Entrypoint Protocol ---"

# 1. Sync Full Codebase
if [ -n "$APP_REPO_URL" ]; then
    GIT_TEMP_DIR="/tmp/app_sync"
    echo "Syncing full codebase from: $APP_REPO_URL"
    
    if [ ! -d "$GIT_TEMP_DIR/.git" ]; then
        echo "Cloning codebase..."
        git clone "$APP_REPO_URL" "$GIT_TEMP_DIR"
    else
        echo "Updating codebase (pulling latest)..."
        cd "$GIT_TEMP_DIR"
        git fetch --all
        git reset --hard origin/main || git reset --hard origin/master
        git pull
        cd - > /dev/null
    fi
    
    echo "Overlaying latest code..."
    cp -R "$GIT_TEMP_DIR/." /app/
    
    echo "Checking for dependency updates..."
    if [ -f "requirements.txt" ]; then
        pip install --no-cache-dir -r requirements.txt
    fi
    
    echo "Codebase synchronization and build complete."
else
    echo "Warning: APP_REPO_URL not set. Running with built-in code."
fi

# 2. Check for OpenAI Key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "CRITICAL: OPENAI_API_KEY is missing! App may fail to start."
fi

# 3. Start Application
echo "Starting PulseAI Application..."
python app.py
