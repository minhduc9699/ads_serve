# Ads Server - Python Flask Application

This is a Python Flask web server that serves 3 ad banners (center, left, right) with dynamic routing for ref_code and image_url parameters.

## Features

- ✅ Dynamic URL routing: `/ads/center.html/ref_code/image_url`
- ✅ Query parameter support: `/ads?file=center&ref_code=abc`
- ✅ No complex nginx configuration needed
- ✅ Easy deployment with gunicorn
- ✅ Systemd service for auto-restart
- ✅ Health check endpoint

## Setup

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2. Deploy to Server

```bash
# Copy files to server
scp -r * your_user@advertnativevn.com:/tmp/ads/

# On server
sudo mkdir -p /var/www/ads
sudo mv /tmp/ads/* /var/www/ads/
cd /var/www/ads

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Make start script executable
chmod +x start.sh
```

### 3. Setup Systemd Service

```bash
# Copy service file
sudo cp ads-server.service /etc/systemd/system/

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable ads-server
sudo systemctl start ads-server

# Check status
sudo systemctl status ads-server
```

### 4. Configure Nginx

Update your nginx configuration:

```bash
sudo nano /etc/nginx/sites-available/advertnativevn.com
```

Add the `/ads` location block to proxy to Flask app (see `ads.conf` for reference).

```bash
# Test and reload nginx
sudo nginx -t
sudo nginx -s reload
```

## Usage

### URL Patterns

#### Path-based routing (recommended):
```
/ads/<filename>.html
/ads/<filename>.html/<ref_code>
/ads/<filename>.html/<ref_code>/<image_url>
```

#### Query parameter routing (alternative):
```
/ads?file=<filename>&ref_code=<code>&image_url=<url>
```

### Parameters

- **filename**: Ad position
  - Valid values: `center`, `left`, `right`
  
- **ref_code**: Shopee affiliate code (optional)
  - Used to build link: `https://s.shopee.vn/${ref_code}`
  
- **image_url**: Custom banner image URL (optional)
  - Can contain slashes, will be URL decoded

### Examples

1. **Basic ad (no parameters):**
   ```
   https://advertnativevn.com/ads/center.html
   ```

2. **Ad with ref_code:**
   ```
   https://advertnativevn.com/ads/left.html/30g9eLlYgx
   ```

3. **Ad with ref_code and custom image:**
   ```
   https://advertnativevn.com/ads/right.html/5VMxs78ckR/https://example.com/banner.jpg
   ```

4. **Query parameter style:**
   ```
   https://advertnativevn.com/ads?file=center&ref_code=abc123&image_url=https://example.com/img.jpg
   ```

### Response Headers

The server includes tracking headers in responses:
- `X-Ref-Code`: The ref_code parameter value
- `X-Image-URL`: The image_url parameter value

## Development

### Run locally:
```bash
source venv/bin/activate
python app.py
```

Server will start on `http://localhost:8089`

### Run with gunicorn:
```bash
./start.sh
```

## File Structure

```
/var/www/ads/
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── start.sh           # Gunicorn start script
├── ads-server.service # Systemd service file
├── ads.conf           # Nginx configuration
├── center.html        # Center banner
├── left.html          # Left banner
├── right.html         # Right banner
└── venv/              # Virtual environment
```

## Testing

```bash
# Health check
curl http://localhost:8089/health

# Test basic ad
curl http://localhost:8089/ads/center.html

# Test with ref_code
curl http://localhost:8089/ads/left.html/30g9eLlYgx -v

# Test with all parameters
curl "http://localhost:8089/ads/right.html/abc123/https://example.com/image.jpg" -v

# Reload templates without restart
curl -X POST http://localhost:8089/ads/reload
```

## Logs

```bash
# View service logs
sudo journalctl -u ads-server -f

# View nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```
