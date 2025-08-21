#!/usr/bin/env python3
"""
Flask Development Server Script
Agent_Cellphone_V2_Repository TDD Integration Project

This script runs the Flask development server with:
- Hot reloading enabled
- Debug mode for development
- Proper configuration loading
- Health monitoring integration

Author: Web Development & UI Framework Specialist
License: MIT
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any

# Add src directory to Python path
repo_root = Path(__file__).parent.parent
src_dir = repo_root / "src"
sys.path.insert(0, str(src_dir))

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import yaml

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FlaskDevelopmentServer:
    """Flask development server for TDD integration"""
    
    def __init__(self, config_path: str = None):
        self.repo_root = Path(__file__).parent.parent
        self.config_path = config_path or str(self.repo_root / "config" / "flask_config.json")
        self.config = self._load_config()
        
        # Initialize Flask app
        self.app = Flask(__name__)
        self.app.config.update(self.config.get('development', {}))
        
        # Setup CORS
        CORS(self.app)
        
        # Setup routes
        self._setup_routes()
        
        logger.info("Flask development server initialized")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load Flask configuration"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            else:
                logger.warning(f"Config file not found: {self.config_path}")
                return self._get_default_config()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default Flask configuration"""
        return {
            "development": {
                "DEBUG": True,
                "TESTING": False,
                "SECRET_KEY": "dev-secret-key-change-in-production",
                "DATABASE_URI": "sqlite:///dev.db",
                "LOG_LEVEL": "DEBUG",
                "HOST": "0.0.0.0",
                "PORT": 5000
            }
        }
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            """Main application page"""
            return render_template('index.html')
        
        @self.app.route('/health')
        def health_check():
            """Health check endpoint"""
            return jsonify({
                'status': 'healthy',
                'service': 'Flask Development Server',
                'version': '2.0.0',
                'environment': 'development'
            })
        
        @self.app.route('/api/status')
        def api_status():
            """API status endpoint"""
            return jsonify({
                'api_status': 'operational',
                'endpoints': [
                    '/health',
                    '/api/status',
                    '/api/web/automation',
                    '/api/web/ui'
                ]
            })
        
        @self.app.route('/api/web/automation', methods=['GET', 'POST'])
        def web_automation():
            """Web automation endpoint"""
            if request.method == 'GET':
                return jsonify({
                    'automation_status': 'ready',
                    'capabilities': [
                        'selenium_webdriver',
                        'playwright',
                        'web_scraping',
                        'form_automation'
                    ]
                })
            else:
                data = request.get_json() or {}
                return jsonify({
                    'message': 'Automation request received',
                    'data': data,
                    'status': 'processing'
                })
        
        @self.app.route('/api/web/ui', methods=['GET', 'POST'])
        def web_ui():
            """Web UI framework endpoint"""
            if request.method == 'GET':
                return jsonify({
                    'ui_framework_status': 'active',
                    'frameworks': [
                        'Flask',
                        'FastAPI',
                        'React (planned)',
                        'Vue.js (planned)'
                    ]
                })
            else:
                data = request.get_json() or {}
                return jsonify({
                    'message': 'UI request received',
                    'data': data,
                    'status': 'processing'
                })
        
        @self.app.route('/test')
        def test_page():
            """Test page for TDD development"""
            return render_template('test.html')
    
    def create_templates(self):
        """Create basic HTML templates for development"""
        templates_dir = self.repo_root / "src" / "web" / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Create base template
        base_template = templates_dir / "base.html"
        if not base_template.exists():
            base_template.write_text("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Agent_Cellphone_V2{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <header>
        <nav>
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/test">Test</a></li>
                <li><a href="/health">Health</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <p>&copy; 2024 Agent_Cellphone_V2 TDD Integration</p>
    </footer>
    
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
</body>
</html>
""")
        
        # Create index template
        index_template = templates_dir / "index.html"
        if not index_template.exists():
            index_template.write_text("""
{% extends "base.html" %}

{% block title %}Agent_Cellphone_V2 - TDD Integration{% endblock %}

{% block content %}
<div class="container">
    <h1>🚀 Agent_Cellphone_V2 TDD Integration</h1>
    <p>Welcome to the Web Development & UI Framework Specialist environment!</p>
    
    <div class="features">
        <div class="feature-card">
            <h3>🌐 Web Automation</h3>
            <p>Selenium WebDriver integration for automated testing</p>
        </div>
        
        <div class="feature-card">
            <h3>🔥 Flask Framework</h3>
            <p>Modern web application development</p>
        </div>
        
        <div class="feature-card">
            <h3>⚡ FastAPI</h3>
            <p>High-performance API development</p>
        </div>
        
        <div class="feature-card">
            <h3>🧪 TDD Testing</h3>
            <p>Test-driven development infrastructure</p>
        </div>
    </div>
    
    <div class="actions">
        <a href="/test" class="btn btn-primary">Run Tests</a>
        <a href="/health" class="btn btn-secondary">Health Check</a>
    </div>
</div>
{% endblock %}
""")
        
        # Create test template
        test_template = templates_dir / "test.html"
        if not test_template.exists():
            test_template.write_text("""
{% extends "base.html" %}

{% block title %}TDD Testing - Agent_Cellphone_V2{% endblock %}

{% block content %}
<div class="container">
    <h1>🧪 TDD Testing Environment</h1>
    <p>Test-driven development infrastructure is ready!</p>
    
    <div class="test-info">
        <h3>Available Test Suites:</h3>
        <ul>
            <li><strong>Unit Tests:</strong> <code>python -m pytest tests/web/unit/ -v</code></li>
            <li><strong>Integration Tests:</strong> <code>python -m pytest tests/web/integration/ -v</code></li>
            <li><strong>Selenium Tests:</strong> <code>python -m pytest tests/web/selenium/ -v</code></li>
            <li><strong>E2E Tests:</strong> <code>python -m pytest tests/web/e2e/ -v</code></li>
        </ul>
    </div>
    
    <div class="test-status">
        <h3>Test Status:</h3>
        <div id="test-results">Loading...</div>
    </div>
</div>

<script>
// Simple test status checker
document.addEventListener('DOMContentLoaded', function() {
    fetch('/health')
        .then(response => response.json())
        .then(data => {
            document.getElementById('test-results').innerHTML = 
                `<span class="status-ok">✅ ${data.status}</span>`;
        })
        .catch(error => {
            document.getElementById('test-results').innerHTML = 
                `<span class="status-error">❌ Error: ${error.message}</span>`;
        });
});
</script>
{% endblock %}
""")
        
        logger.info("HTML templates created successfully")
    
    def create_static_files(self):
        """Create basic CSS and JavaScript files"""
        static_dir = self.repo_root / "src" / "web" / "static"
        
        # Create CSS file
        css_dir = static_dir / "css"
        css_dir.mkdir(parents=True, exist_ok=True)
        
        css_file = css_dir / "style.css"
        if not css_file.exists():
            css_file.write_text("""
/* Agent_Cellphone_V2 TDD Integration Styles */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f4f4f4;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

header {
    background-color: #2c3e50;
    color: white;
    padding: 1rem 0;
}

nav ul {
    list-style: none;
    display: flex;
    justify-content: center;
}

nav ul li {
    margin: 0 15px;
}

nav ul li a {
    color: white;
    text-decoration: none;
    padding: 5px 10px;
    border-radius: 3px;
    transition: background-color 0.3s;
}

nav ul li a:hover {
    background-color: #34495e;
}

.features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin: 30px 0;
}

.feature-card {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    text-align: center;
}

.feature-card h3 {
    color: #2c3e50;
    margin-bottom: 10px;
}

.actions {
    text-align: center;
    margin: 30px 0;
}

.btn {
    display: inline-block;
    padding: 10px 20px;
    margin: 0 10px;
    text-decoration: none;
    border-radius: 5px;
    transition: background-color 0.3s;
}

.btn-primary {
    background-color: #3498db;
    color: white;
}

.btn-primary:hover {
    background-color: #2980b9;
}

.btn-secondary {
    background-color: #95a5a6;
    color: white;
}

.btn-secondary:hover {
    background-color: #7f8c8d;
}

.test-info {
    background: white;
    padding: 20px;
    border-radius: 8px;
    margin: 20px 0;
}

.test-info ul {
    margin: 15px 0;
    padding-left: 20px;
}

.test-info code {
    background-color: #f8f9fa;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
}

.status-ok {
    color: #27ae60;
    font-weight: bold;
}

.status-error {
    color: #e74c3c;
    font-weight: bold;
}

footer {
    text-align: center;
    padding: 20px;
    color: #7f8c8d;
    margin-top: 50px;
}
""")
        
        # Create JavaScript file
        js_dir = static_dir / "js"
        js_dir.mkdir(parents=True, exist_ok=True)
        
        js_file = js_dir / "app.js"
        if not js_file.exists():
            js_file.write_text("""
// Agent_Cellphone_V2 TDD Integration JavaScript

console.log('🚀 Agent_Cellphone_V2 TDD Integration loaded!');

// Add some interactive functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing app...');
    
    // Add click handlers for feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('click', function() {
            this.style.transform = 'scale(1.05)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 200);
        });
    });
    
    // Add smooth scrolling for navigation
    const navLinks = document.querySelectorAll('nav a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});
""")
        
        logger.info("Static files created successfully")
    
    def run(self):
        """Run the Flask development server"""
        try:
            # Create templates and static files
            self.create_templates()
            self.create_static_files()
            
            # Get server configuration
            host = self.config.get('development', {}).get('HOST', '0.0.0.0')
            port = self.config.get('development', {}).get('PORT', 5000)
            debug = self.config.get('development', {}).get('DEBUG', True)
            
            logger.info(f"Starting Flask development server on {host}:{port}")
            logger.info(f"Debug mode: {debug}")
            logger.info(f"Open http://localhost:{port} in your browser")
            
            # Run the Flask app
            self.app.run(
                host=host,
                port=port,
                debug=debug,
                use_reloader=True
            )
            
        except Exception as e:
            logger.error(f"Error running Flask server: {e}")
            sys.exit(1)

def main():
    """Main function to run Flask development server"""
    try:
        server = FlaskDevelopmentServer()
        server.run()
    except KeyboardInterrupt:
        logger.info("Flask development server stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
