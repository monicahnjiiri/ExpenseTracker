#!/usr/bin/env python3
"""
🚀 ExpenseTracker Multi-User Application Launcher
This script starts both the web application and the automation system.
"""

import os
import sys
import threading
import time

def start_automation():
    """Start the automation system in a separate thread"""
    print("🤖 Starting automation system...")
    try:
        from src.automation import start_automation
        start_automation()
    except Exception as e:
        print(f"⚠️ Could not start automation: {e}")
        print("📧 Email alerts will not be sent automatically")

def start_web_app():
    """Start the Flask web application"""
    print("🌐 Starting web application...")
    try:
        from src.webapp import app, init_db
        
        # Initialize database
        init_db()
        print("📁 Database initialized")
        
        # Start automation in background
        automation_thread = threading.Thread(target=start_automation, daemon=True)
        automation_thread.start()
        
        print("\n" + "="*60)
        print("🎉 EXPENSETRACKER MULTI-USER APP READY!")
        print("="*60)
        print("📱 Open your browser and go to: http://localhost:5000")
        print("👥 Multiple users can register and track expenses")
        print("📧 Automated weekly/monthly alerts for all users")
        print("💡 To enable email alerts:")
        print("   1. Edit email_service.py")
        print("   2. Set your Gmail credentials")
        print("   3. Set EMAIL_ENABLED = True")
        print("="*60)
        print("Press Ctrl+C to stop the application")
        print("="*60 + "\n")
        
        # Get port from environment (for cloud hosting)
        import os
        port = int(os.environ.get('PORT', 5000))
        
        # Start Flask app
        app.run(debug=False, host='0.0.0.0', port=port)
        
    except Exception as e:
        print(f"❌ Error starting web app: {e}")
        return False

if __name__ == "__main__":
    print("🚀 ExpenseTracker Multi-User App Starting...")
    print("💰 Your complete financial tracking solution")
    print("-" * 50)
    
    try:
        start_web_app()
    except KeyboardInterrupt:
        print("\n👋 ExpenseTracker stopped. Have a great day!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
