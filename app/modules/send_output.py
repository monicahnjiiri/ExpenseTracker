# send the results to the user
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
from datetime import datetime

def send_result(user_info, result):
    """
    Send the processed results to the user.
    This function can be extended to send emails, save to a file, etc.
    """
    print("\n=== EXPENSE TRACKER RESULTS ===")
    
    # Display results if available
    if isinstance(result, dict):
        print("\nFinancial Summary:")
        if 'weekly_expenses' in result:
            weekly_expenses = result['weekly_expenses']
            total_weekly_expenses = weekly_expenses.sum() if hasattr(weekly_expenses, 'sum') else 0
            print(f"Total Weekly Expenses: {total_weekly_expenses:.2f}")
        
        if 'monthly_income' in result:
            monthly_income = result['monthly_income']
            total_monthly_income = monthly_income.sum() if hasattr(monthly_income, 'sum') else 0
            print(f"Total Monthly Income: {total_monthly_income:.2f}")
        
        if 'monthly_savings' in result:
            print(f"Monthly Savings: {result['monthly_savings']:.2f}")
        
        if 'tax_due' in result:
            print(f"Estimated Tax Due: {result['tax_due']:.2f}")
    
    # Send email alerts when expenses exceed budget
    budget = user_info.get("budget", 0)
    
    # Calculate total expenses from result
    total_expenses = 0
    if isinstance(result, dict) and 'weekly_expenses' in result:
        weekly_expenses = result['weekly_expenses']
        total_expenses = weekly_expenses.sum() if hasattr(weekly_expenses, 'sum') else 0
    
    if total_expenses > budget:
        print(f"\n[ALERT] Your expenses ({total_expenses:.2f}) exceed your budget ({budget:.2f}).")
    else:
        print(f"\n[INFO] Your expenses ({total_expenses:.2f}) are within your budget ({budget:.2f}).")
    
    # Send the results to the given user email from user_input
    email = user_info.get("email", "")
    if email:
        print(f"\nSending results to {email}...")
        
        # Save user info for automated alerts
        save_user_config(user_info)
        
        # Send email with results
        send_email_alert(user_info, result, total_expenses, budget)
        
        print("Results sent successfully!")
    else:
        print("\n[ERROR] No email address provided.")

def save_user_config(user_info):
    """Save user configuration for automation"""
    try:
        os.makedirs('config', exist_ok=True)
        with open('config/user_config.json', 'w') as f:
            json.dump(user_info, f, indent=4)
    except Exception as e:
        print(f"Warning: Could not save user config: {e}")

def send_email_alert(user_info, result, total_expenses, budget):
    """Send email alert with results"""
    try:
        # Email configuration (you can modify these)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "your_email@gmail.com"  # Replace with your email
        sender_password = "your_app_password"  # Replace with your app password
        
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"💰 ExpenseTracker Alert - {datetime.now().strftime('%B %d, %Y')}"
        msg["From"] = sender_email
        msg["To"] = user_info.get('email')
        
        # Create HTML content
        status = "Budget Exceeded ⚠️" if total_expenses > budget else "Within Budget ✅"
        status_color = "#e74c3c" if total_expenses > budget else "#27ae60"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: {status_color}; text-align: center;">
                    ExpenseTracker Report
                </h2>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3>Hello {user_info.get('name', 'User')}!</h3>
                    
                    <div style="background-color: {status_color}; color: white; padding: 15px; border-radius: 5px; text-align: center; margin: 15px 0;">
                        <h3 style="margin: 0;">{status}</h3>
                    </div>
                    
                    <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                        <tr style="background-color: #e9ecef;">
                            <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">Total Expenses:</td>
                            <td style="padding: 10px; border: 1px solid #ddd;">€{total_expenses:.2f}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">Weekly Budget:</td>
                            <td style="padding: 10px; border: 1px solid #ddd;">€{budget:.2f}</td>
                        </tr>
                        <tr style="background-color: #e9ecef;">
                            <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">Difference:</td>
                            <td style="padding: 10px; border: 1px solid #ddd; color: {status_color};">
                                €{total_expenses - budget:.2f}
                            </td>
                        </tr>
        """
        
        # Add monthly data if available
        if isinstance(result, dict):
            if 'monthly_income' in result:
                monthly_income = result['monthly_income'].sum() if hasattr(result['monthly_income'], 'sum') else 0
                html_content += f"""
                        <tr>
                            <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">Monthly Income:</td>
                            <td style="padding: 10px; border: 1px solid #ddd;">€{monthly_income:.2f}</td>
                        </tr>
                """
            
            if 'monthly_savings' in result:
                html_content += f"""
                        <tr style="background-color: #e9ecef;">
                            <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">Monthly Savings:</td>
                            <td style="padding: 10px; border: 1px solid #ddd;">€{result['monthly_savings']:.2f}</td>
                        </tr>
                """
            
            if 'tax_due' in result:
                html_content += f"""
                        <tr>
                            <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">Estimated Tax:</td>
                            <td style="padding: 10px; border: 1px solid #ddd;">€{result['tax_due']:.2f}</td>
                        </tr>
                """
        
        html_content += """
                    </table>
                </div>
                
                <p style="text-align: center; color: #666; font-size: 12px;">
                    This is an automated message from your ExpenseTracker system.
                </p>
            </div>
        </body>
        </html>
        """
        
        # Attach HTML content
        html_part = MIMEText(html_content, "html")
        msg.attach(html_part)
        
        # Send email (disabled for now - set EMAIL_ENABLED = True to activate)
        EMAIL_ENABLED = False  # Change to True when you configure your email
        
        if EMAIL_ENABLED:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
            print(f"✅ Email sent to {user_info.get('email')}")
        else:
            print(f"[EMAIL DISABLED] Would send email to {user_info.get('email')}")
            print(f"Status: {status}")
            
    except Exception as e:
        print(f"Error sending email: {e}")

# Simple automation functions using your existing pipeline
def setup_automation():
    """Setup automated weekly and monthly alerts"""
    try:
        import schedule
        import time
        import threading
        
        def weekly_alert():
            """Run weekly analysis and send alert"""
            print("� Running weekly automated check...")
            try:
                from modules.fetch_csv import read_csv_data
                from modules.process_data import manipulate_data
                
                # Load user config
                with open('config/user_config.json', 'r') as f:
                    user_info = json.load(f)
                
                # Load and process data
                expense_data = read_csv_data("data/Expenses.csv")
                income_data = read_csv_data("data/Income.csv")
                
                if not expense_data.empty:
                    result = manipulate_data(expense_data, income_data, user_info)
                    send_result(user_info, result)
                    
            except Exception as e:
                print(f"Error in weekly alert: {e}")
        
        def monthly_report():
            """Run monthly analysis and send report"""
            print("📊 Running monthly automated report...")
            weekly_alert()  # Same process, just different timing
        
        # Schedule the alerts
        schedule.every().sunday.at("20:00").do(weekly_alert)  # Every Sunday 8 PM
        schedule.every().day.at("09:00").do(monthly_report)  # Check daily for 1st of month
        
        def run_scheduler():
            while True:
                schedule.run_pending()
                # Check if it's the 1st of the month for monthly report
                from datetime import datetime
                if datetime.now().day == 1 and datetime.now().hour == 9:
                    monthly_report()
                time.sleep(60)  # Check every minute
        
        # Run scheduler in background
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        
        print("✅ Automation started!")
        print("📧 Weekly alerts: Every Sunday at 8:00 PM")
        print("📊 Monthly reports: 1st of each month")
        
        return scheduler_thread
        
    except ImportError:
        print("⚠️ Install 'schedule' package for automation: pip install schedule")
        return None
    except Exception as e:
        print(f"Error setting up automation: {e}")
        return None
