#!/bin/bash

NGINX_CONF_SOURCE="nginx.conf"
NGINX_CONF_DEST="/etc/nginx/sites-available/mgrzmil.dev"

# Check if source file exists
if [ ! -f "$NGINX_CONF_SOURCE" ]; then
    echo "Error: $NGINX_CONF_SOURCE not found in current directory"
    exit 1
fi

# Copy configuration file
echo "Copying $NGINX_CONF_SOURCE to $NGINX_CONF_DEST..."
sudo cp "$NGINX_CONF_SOURCE" "$NGINX_CONF_DEST"

# Test nginx configuration
echo "Testing nginx configuration..."
sudo nginx -t

# If test passes, reload nginx
if [ $? -eq 0 ]; then
    echo "Configuration test passed. Reloading nginx..."
    sudo systemctl reload nginx
    echo "Nginx reloaded successfully"
else
    echo "Nginx configuration test failed. Please fix errors before reloading."
    exit 1
fi
