#!/usr/bin/env python3
"""
Production WSGI entry point for Render deployment
"""
import os
from simple_run import app

# Production configuration
app.config.update(
    DEBUG=False,
    SECRET_KEY=os.environ.get('SECRET_KEY', 'render-production-secret-key-change-this'),
    ENV='production'
)

if __name__ == "__main__":
    # Get port from environment variable (Render sets this automatically)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
