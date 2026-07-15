#!/bin/bash

# 9Hits Viewer starter for Railway
# Handles TTY and network constraints

echo "Starting 9Hits Viewer..."
echo "Access Key: ${NH_ACCESS_KEY:0:8}..."

# Check if we can allocate TTY
if [ -t 0 ]; then
    echo "TTY available - running normally"
else
    echo "No TTY - running with script wrapper"
fi

# Run the viewer with our config
exec /nh.sh \
    --access-key="$NH_ACCESS_KEY" \
    --system-session \
    --hide-browser=yes \
    --allow-crypto=no \
    --allow-adult=no \
    --cache-limit=0 \
    --note="railway-9hits" \
    --session-note="aliexhelper-traffic"
