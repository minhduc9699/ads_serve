#!/usr/bin/env python3
"""
Ads Server - Python Flask web server for serving ad banners
Handles dynamic routing for /ads endpoints with ref_code and image_url parameters
"""

from flask import Flask, render_template_string, request, make_response
import os
from urllib.parse import unquote

app = Flask(__name__)

# Load HTML templates
def load_html_file(filename):
    """Load HTML file content"""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

# Cache HTML templates
HTML_TEMPLATES = {}

def get_template(ad_type):
    """Get cached HTML template for ad type"""
    if ad_type not in HTML_TEMPLATES:
        HTML_TEMPLATES[ad_type] = load_html_file(f'{ad_type}.html')
    return HTML_TEMPLATES[ad_type]


@app.route('/ads/<ad_type>.html', methods=['GET'])
@app.route('/ads/<ad_type>.html/<ref_code>', methods=['GET'])
@app.route('/ads/<ad_type>.html/<ref_code>/<path:image_url>', methods=['GET'])
def serve_ad(ad_type, ref_code=None, image_url=None):
    """
    Serve ad HTML with optional ref_code and image_url
    
    URL patterns:
    - /ads/center.html
    - /ads/center.html/ref_code
    - /ads/center.html/ref_code/image_url
    """
    # Validate ad type
    if ad_type not in ['center', 'left', 'right']:
        return "Invalid ad type. Must be: center, left, or right", 400
    
    # Get HTML template
    try:
        html_content = get_template(ad_type)
    except FileNotFoundError:
        return f"Ad template '{ad_type}.html' not found", 404
    
    # Decode image_url if present
    if image_url:
        image_url = unquote(image_url)
    
    # Create response
    response = make_response(html_content)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    
    # Add custom headers for tracking
    if ref_code:
        response.headers['X-Ref-Code'] = ref_code
    if image_url:
        response.headers['X-Image-URL'] = image_url
    
    return response


@app.route('/ads', methods=['GET'])
def serve_ad_query_params():
    """
    Serve ad HTML using query parameters (alternative approach)
    
    URL pattern:
    - /ads?file=center&ref_code=abc123&image_url=https://example.com/image.jpg
    """
    # Get query parameters
    ad_type = request.args.get('file', 'center')
    ref_code = request.args.get('ref_code', '')
    image_url = request.args.get('image_url', '')
    
    # Validate ad type
    if ad_type not in ['center', 'left', 'right']:
        return "Invalid file parameter. Must be: center, left, or right", 400
    
    # Get HTML template
    try:
        html_content = get_template(ad_type)
    except FileNotFoundError:
        return f"Ad template '{ad_type}.html' not found", 404
    
    # Create response
    response = make_response(html_content)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    
    # Add custom headers for tracking
    if ref_code:
        response.headers['X-Ref-Code'] = ref_code
    if image_url:
        response.headers['X-Image-URL'] = image_url
    
    return response


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return 'OK', 200


@app.route('/ads/reload', methods=['POST'])
def reload_templates():
    """Reload HTML templates (useful for updates without restart)"""
    global HTML_TEMPLATES
    HTML_TEMPLATES = {}
    return 'Templates reloaded', 200


if __name__ == '__main__':
    # Load templates on startup
    for ad_type in ['center', 'left', 'right']:
        try:
            get_template(ad_type)
            print(f"✓ Loaded template: {ad_type}.html")
        except FileNotFoundError:
            print(f"✗ Warning: {ad_type}.html not found")
    
    # Run server
    print("\n🚀 Ads Server starting...")
    print("📍 Listening on http://0.0.0.0:8089")
    print("\nEndpoints:")
    print("  - /ads/center.html")
    print("  - /ads/center.html/ref_code")
    print("  - /ads/center.html/ref_code/image_url")
    print("  - /ads?file=center&ref_code=abc&image_url=https://...")
    print("  - /health")
    print("\n")
    
    app.run(host='0.0.0.0', port=8089, debug=False)
