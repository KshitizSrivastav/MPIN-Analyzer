#!/usr/bin/env python3
"""
Minimal Production WSGI for Render
"""
import os
import sys
from datetime import datetime

# Production environment setup
os.environ['FLASK_ENV'] = 'production'

try:
    from flask import Flask, render_template, request, jsonify
    from app import MPINChecker
    
    # Create minimal Flask app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'render-production-key')
    app.config['DEBUG'] = False
    
    # Essential health check
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'service': 'MPIN Analyzer'}
    
    @app.route('/ping')
    def ping():
        return 'pong'
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/debug')
    def debug():
        return render_template('simple_debug.html')
    
    @app.route('/simple-debug')
    def simple_debug():
        return render_template('simple_debug.html')
    
    @app.route('/api/check_mpin', methods=['POST'])
    def check_mpin():
        try:
            data = request.get_json()
            pin = data.get('pin', '').strip()
            
            # Basic validation
            if not pin or not pin.isdigit() or len(pin) not in [4, 6]:
                return jsonify({'success': False, 'error': 'Invalid PIN format'})
            
            # Create checker
            checker = MPINChecker(digit_length=len(pin))
            birth_date = data.get('birth_date', '').strip() or None
            spouse_birth_date = data.get('spouse_birth_date', '').strip() or None
            wedding_date = data.get('wedding_date', '').strip() or None
            
            strength, reasons = checker.check_strength(pin, birth_date, spouse_birth_date, wedding_date)
            is_common = checker.is_common(pin)
            
            # Simple analysis
            score = 100 if strength == "STRONG" else (50 if strength == "MODERATE" else 20)
            recommendations = ["Use random digits", "Avoid personal dates"] if strength != "STRONG" else ["Good choice!"]
            
            return jsonify({
                'success': True,
                'pin': pin,
                'strength': strength,
                'reasons': reasons,
                'is_common': is_common,
                'analysis': {
                    'strength_score': score,
                    'recommendations': recommendations,
                    'demographic_matches': [],
                    'common_patterns': []
                }
            })
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    if __name__ == "__main__":
        port = int(os.environ.get('PORT', 5000))
        print(f"🚀 Starting MPIN Analyzer on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False)

except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
