#!/usr/bin/env python3
"""
Simple MPIN Web App Launcher - No Virtual Environment Required
This script runs the MPIN analyzer directly with system Python
"""

import os
import sys

# Detect if running on Render (production) or locally (development)
is_production = os.environ.get('PORT') is not None or os.environ.get('RENDER') is not None

if is_production:
    os.environ['FLASK_ENV'] = 'production'
else:
    os.environ['FLASK_ENV'] = 'development'

try:
    from flask import Flask, render_template, request, jsonify
    from datetime import datetime
    import json
    
    # Import the MPINChecker class from the existing app.py
    from app import MPINChecker
    
    # Create Flask app directly
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'development-secret-key')
    app.config['DEBUG'] = not is_production  # Only debug in development
    
    @app.route('/')
    def index():
        """Main page with MPIN strength checker interface"""
        return render_template('index.html')
    
    @app.route('/health')
    def health_check():
        """Health check endpoint for Render"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'MPIN Analyzer',
            'environment': os.environ.get('FLASK_ENV', 'unknown')
        })
    
    @app.route('/ping')
    def ping():
        """Simple ping endpoint"""
        return 'pong'
    
    @app.route('/debug')
    def debug():
        """Debug test page for MPIN analysis"""
        return render_template('simple_debug.html')
    
    @app.route('/simple-debug')
    def simple_debug():
        """Simple debug page for testing"""
        return render_template('simple_debug.html')
    
    @app.route('/api/check_mpin', methods=['POST'])
    def check_mpin():
        """API endpoint to check MPIN strength"""
        try:
            data = request.get_json()
            
            # Extract data from request
            pin = data.get('pin', '').strip()
            digit_length = len(pin) if pin.isdigit() else 4
            birth_date = data.get('birth_date', '').strip() or None
            spouse_birth_date = data.get('spouse_birth_date', '').strip() or None
            wedding_date = data.get('wedding_date', '').strip() or None
            
            # Validate PIN
            if not pin:
                return jsonify({
                    'success': False,
                    'error': 'Please enter a PIN'
                })
            
            if not pin.isdigit():
                return jsonify({
                    'success': False,
                    'error': 'PIN must contain only digits'
                })
            
            if len(pin) not in [4, 6]:
                return jsonify({
                    'success': False,
                    'error': 'PIN must be 4 or 6 digits long'
                })
            
            # Create checker and analyze PIN
            checker = MPINChecker(digit_length=len(pin))
            strength, reasons = checker.check_strength(pin, birth_date, spouse_birth_date, wedding_date)
            
            # Check if it's commonly used
            is_common = checker.is_common(pin)
            
            # Get detailed analysis
            analysis = get_detailed_analysis(pin, strength, reasons, is_common, checker, 
                                           birth_date, spouse_birth_date, wedding_date)
            
            return jsonify({
                'success': True,
                'pin': pin,
                'strength': strength,
                'reasons': reasons,
                'is_common': is_common,
                'analysis': analysis
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'An error occurred: {str(e)}'
            })
    
    def get_detailed_analysis(pin, strength, reasons, is_common, checker, birth_date, spouse_birth_date, wedding_date):
        """Get detailed analysis of the PIN"""
        analysis = {
            'length_analysis': f"Your PIN is {len(pin)} digits long.",
            'strength_score': get_strength_score(strength, reasons),
            'recommendations': get_recommendations(strength, reasons),
            'demographic_matches': [],
            'common_patterns': []
        }
        
        # Check for demographic matches
        if birth_date:
            birth_combinations = checker.generate_demographic_combinations(birth_date)
            if pin in birth_combinations:
                analysis['demographic_matches'].append(f"Matches your birth date ({birth_date})")
        
        if spouse_birth_date:
            spouse_combinations = checker.generate_demographic_combinations(spouse_birth_date)
            if pin in spouse_combinations:
                analysis['demographic_matches'].append(f"Matches spouse's birth date ({spouse_birth_date})")
        
        if wedding_date:
            wedding_combinations = checker.generate_demographic_combinations(wedding_date)
            if pin in wedding_combinations:
                analysis['demographic_matches'].append(f"Matches wedding date ({wedding_date})")
        
        # Check for common patterns
        if is_common:
            if pin == pin[0] * len(pin):
                analysis['common_patterns'].append("All digits are the same")
            elif is_sequential(pin):
                analysis['common_patterns'].append("Sequential digits pattern")
            elif is_repeating_pattern(pin):
                analysis['common_patterns'].append("Repeating digit pattern")
        
        return analysis
    
    def get_strength_score(strength, reasons):
        """Calculate a numerical strength score"""
        if strength == "STRONG":
            return 100
        elif strength == "WEAK":
            return max(20, 80 - len(reasons) * 20)
        else:
            return 0
    
    def get_recommendations(strength, reasons):
        """Get recommendations based on analysis"""
        recommendations = []
        
        if "COMMONLY_USED" in reasons:
            recommendations.append("Avoid commonly used PINs like 1111, 1234, or 0000")
        
        if "DEMOGRAPHIC_DOB_SELF" in reasons:
            recommendations.append("Don't use your birth date in your PIN")
        
        if "DEMOGRAPHIC_DOB_SPOUSE" in reasons:
            recommendations.append("Don't use your spouse's birth date in your PIN")
        
        if "DEMOGRAPHIC_ANNIVERSARY" in reasons:
            recommendations.append("Don't use your wedding/anniversary date in your PIN")
        
        if strength == "STRONG":
            recommendations.append("Great choice! This PIN appears to be strong and secure.")
        else:
            recommendations.extend([
                "Use a mix of digits that don't follow obvious patterns",
                "Avoid personal information like dates",
                "Consider using a random combination of digits"
            ])
        
        return recommendations
    
    def is_sequential(pin):
        """Check if PIN has sequential digits"""
        for i in range(len(pin) - 1):
            if int(pin[i+1]) != (int(pin[i]) + 1) % 10:
                return False
        return True
    
    def is_repeating_pattern(pin):
        """Check if PIN has repeating patterns"""
        if len(pin) == 4:
            return pin[:2] == pin[2:4]
        elif len(pin) == 6:
            return pin[:2] == pin[2:4] == pin[4:6] or pin[:3] == pin[3:6]
        return False
    
    @app.route('/api/test_cases')
    def run_test_cases():
        """API endpoint to run all test cases"""
        try:
            # Sample test cases
            test_cases = [
                {"part": "A", "digit_length": 4, "pin": "1111", "expected": True},
                {"part": "A", "digit_length": 4, "pin": "1234", "expected": True},
                {"part": "A", "digit_length": 4, "pin": "4839", "expected": False},
                {"part": "B", "digit_length": 4, "pin": "1111", "birth_date": None, "spouse_birth_date": None, "wedding_date": None, "expected": "WEAK"},
                {"part": "B", "digit_length": 4, "pin": "4839", "birth_date": "02-01-1998", "spouse_birth_date": "15-06-1995", "wedding_date": "10-07-2020", "expected": "STRONG"},
            ]
            
            test_results = []
            for test_index, test in enumerate(test_cases, 1):
                checker = MPINChecker(digit_length=test["digit_length"])
                pin = test["pin"]
                result = {"test_number": test_index, "pin": pin, "part": test["part"]}
                
                try:
                    if test["part"] == "A":
                        actual = checker.is_common(pin)
                        expected = test["expected"]
                        result["expected"] = expected
                        result["actual"] = actual
                        result["passed"] = actual == expected
                    elif test["part"] == "B":
                        birth_date = test.get("birth_date")
                        spouse_birth_date = test.get("spouse_birth_date")
                        wedding_date = test.get("wedding_date")
                        actual = checker.check_strength(pin, birth_date, spouse_birth_date, wedding_date)[0]
                        expected = test["expected"]
                        result["expected"] = expected
                        result["actual"] = actual
                        result["passed"] = actual == expected
                    
                    test_results.append(result)
                except Exception as e:
                    result["error"] = str(e)
                    result["passed"] = False
                    test_results.append(result)
            
            passed_count = sum(1 for test in test_results if test.get("passed", False))
            total_count = len(test_results)
            
            return jsonify({
                'success': True,
                'results': test_results,
                'summary': {
                    'total': total_count,
                    'passed': passed_count,
                    'failed': total_count - passed_count,
                    'success_rate': f"{(passed_count/total_count)*100:.1f}%"
                }
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Error running test cases: {str(e)}'
            })
    
    def main():
        # Get port from environment (Render sets this automatically)
        port = int(os.environ.get('PORT', 5000))
        host = '0.0.0.0'
        
        if is_production:
            print(f"� Starting MPIN Analyzer in PRODUCTION mode")
            print(f"🌐 Server starting on {host}:{port}")
            print("=" * 60)
            # Production settings - no debug output
            app.run(host=host, port=port, debug=False, threaded=True)
        else:
            print("�🛡️  MPIN Strength Analyzer - Simple Launcher")
            print("=" * 60)
            print("🐍 Using System Python (No Virtual Environment)")
            print("🌐 Starting web application...")
            print("📋 Flask app configured for development")
            print("🔒 Using default secret key for development")
            print("=" * 60)
            print("🌐 Application will be available at:")
            print("   http://localhost:5000")
            print("   http://127.0.0.1:5000")
            print("=" * 60)
            print("🎯 Features:")
            print("   • MPIN Strength Analysis")
            print("   • Common Pattern Detection") 
            print("   • Demographic Information Checking")
            print("   • Test Case Validation")
            print("   • Security Recommendations")
            print("=" * 60)
            print("Press Ctrl+C to stop the server")
            print("=" * 60)
            
        try:
            app.run(host=host, port=port, debug=not is_production)
        except KeyboardInterrupt:
            print("\n👋 Thank you for using MPIN Strength Analyzer!")
            print("Application stopped.")
        except Exception as e:
            print(f"\n❌ Error starting application: {e}")
            sys.exit(1)

    if __name__ == '__main__':
        main()

except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("💡 Please install Flask:")
    print("   pip install Flask==2.3.3 Werkzeug==2.3.7 Jinja2==3.1.2")
    print("   Then run: python simple_run.py")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
