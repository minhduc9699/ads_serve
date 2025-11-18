# Deployment Guide - Ads Server

## Quick Deploy to Server

### 1. Upload Files to Server

```bash
# From your local machine (in /Users/ducpm/ads/)
scp -r app.py requirements.txt start.sh ads-server.service center.html left.html right.html your_user@advertnativevn.com:/tmp/ads/
```

### 2. Setup on Server

```bash
# SSH into your server
ssh your_user@advertnativevn.com

# Move files to proper location
sudo mkdir -p /var/www/ads
sudo mv /tmp/ads/* /var/www/ads/
cd /var/www/ads

# Create virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Make start script executable
chmod +x start.sh

# Set proper permissions
sudo chown -R www-data:www-data /var/www/ads
```

### 3. Setup Systemd Service

```bash
# Copy service file
sudo cp /var/www/ads/ads-server.service /etc/systemd/system/

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable ads-server
sudo systemctl start ads-server

# Check status
sudo systemctl status ads-server
```

### 4. Update Nginx Configuration

```bash
# Edit nginx config
sudo nano /etc/nginx/sites-available/advertnativevn.com
```

Replace the complex `/ads` location blocks with this simple proxy:

```nginx
# Proxy all /ads requests to Python Flask server
location /ads {
    proxy_pass http://localhost:8089;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_redirect off;
}
```

Test and reload nginx:

```bash
sudo nginx -t
sudo nginx -s reload
```

### 5. Verify Deployment

```bash
# Check service status
sudo systemctl status ads-server

# Check logs
sudo journalctl -u ads-server -n 50

# Test locally on server
curl http://localhost:8089/health
curl http://localhost:8089/ads/center.html

# Test from outside
curl https://advertnativevn.com/ads/center.html
curl https://advertnativevn.com/ads/left.html/30g9eLlYgx
```

## Managing the Service

### View Logs
```bash
# Real-time logs
sudo journalctl -u ads-server -f

# Last 100 lines
sudo journalctl -u ads-server -n 100
```

### Restart Service
```bash
sudo systemctl restart ads-server
```

### Stop Service
```bash
sudo systemctl stop ads-server
```

### Update HTML Files
After updating HTML files:
```bash
# Option 1: Reload templates without restart
curl -X POST http://localhost:8089/ads/reload

# Option 2: Restart service
sudo systemctl restart ads-server
```

## Troubleshooting

### Service won't start
```bash
# Check status and errors
sudo systemctl status ads-server
sudo journalctl -u ads-server -n 50

# Check if port 8089 is already in use
sudo netstat -tulpn | grep 8089
```

### 404 Errors
```bash
# Verify HTML files exist
ls -la /var/www/ads/*.html

# Check permissions
ls -la /var/www/ads/

# Should be owned by www-data
sudo chown -R www-data:www-data /var/www/ads
```

### Nginx Issues
```bash
# Test nginx config
sudo nginx -t

# Check nginx error logs
sudo tail -f /var/log/nginx/error.log

# Verify proxy is working
curl -v http://localhost:8089/ads/center.html
```

## URLs Supported

After deployment, these URLs will work:

1. **Basic**: `https://advertnativevn.com/ads/center.html`
2. **With ref_code**: `https://advertnativevn.com/ads/left.html/30g9eLlYgx`
3. **With both params**: `https://advertnativevn.com/ads/right.html/abc123/https://example.com/image.jpg`
4. **Query params**: `https://advertnativevn.com/ads?file=center&ref_code=abc123`

## Benefits of This Approach

✅ **Simple nginx config** - Just one proxy block, no complex regex patterns
✅ **Easy updates** - Modify Python code without touching nginx
✅ **Better logging** - Application-level logs via journalctl
✅ **Scalable** - Can run multiple workers with gunicorn
✅ **Maintainable** - All routing logic in one Python file
