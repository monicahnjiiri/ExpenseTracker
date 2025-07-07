import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

def send_email_alert(user_info, result, total_expenses, budget, alert_type="Weekly Summary"):
    """Send email alert with financial results to user"""
    try:
        # Email configuration - Use environment variables in production
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.environ.get('SENDER_EMAIL', 'your_email@gmail.com')
        sender_password = os.environ.get('SENDER_PASSWORD', 'your_app_password')
        
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"💰 {alert_type} - ExpenseTracker ({datetime.now().strftime('%B %d, %Y')})"
        msg["From"] = sender_email
        msg["To"] = user_info.get('email')
        
        # Determine status
        status = "Budget Exceeded ⚠️" if total_expenses > budget and budget > 0 else "Within Budget ✅"
        status_color = "#e74c3c" if total_expenses > budget and budget > 0 else "#27ae60"
        
        # Create beautiful HTML email
        html_content = f"""
        <html>
        <body style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0;">
            <div style="max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px;">
                <div style="background: white; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
                    
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #667eea; margin: 0; font-size: 28px;">💰 ExpenseTracker</h1>
                        <h2 style="color: {status_color}; margin: 10px 0 0 0; font-size: 20px;">{alert_type}</h2>
                        <p style="color: #666; margin: 5px 0 0 0;">Hello {user_info.get('name', 'User')}!</p>
                    </div>
                    
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr style="background: {status_color}; color: white;">
                                <td style="padding: 15px; font-weight: bold; border-radius: 5px 0 0 5px;">Status</td>
                                <td style="padding: 15px; border-radius: 0 5px 5px 0;">{status}</td>
                            </tr>
        """
        
        # Add financial data
        if isinstance(result, dict):
            if 'weekly_expenses' in result:
                html_content += f"""
                            <tr>
                                <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">Weekly Expenses:</td>
                                <td style="padding: 10px; border: 1px solid #ddd;">${result['weekly_expenses']:.2f}</td>
                            </tr>
                """
            
            if 'monthly_expenses' in result:
                html_content += f"""
                            <tr style="background-color: #f8f9fa;">
                                <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">Monthly Expenses:</td>
                                <td style="padding: 10px; border: 1px solid #ddd;">${result['monthly_expenses']:.2f}</td>
                            </tr>
                """
            
            if 'monthly_income' in result:
                html_content += f"""
                            <tr>
                                <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">Monthly Income:</td>
                                <td style="padding: 10px; border: 1px solid #ddd;">${result['monthly_income']:.2f}</td>
                            </tr>
                """
            
            if 'monthly_savings' in result:
                savings_color = "#27ae60" if result['monthly_savings'] >= 0 else "#e74c3c"
                savings_text = "Savings" if result['monthly_savings'] >= 0 else "Deficit"
                html_content += f"""
                            <tr style="background-color: #e9ecef;">
                                <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">Monthly {savings_text}:</td>
                                <td style="padding: 10px; border: 1px solid #ddd; color: {savings_color}; font-weight: bold;">${abs(result['monthly_savings']):.2f}</td>
                            </tr>
                """
        
        # Add budget information
        if budget > 0:
            html_content += f"""
                            <tr>
                                <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">Monthly Budget:</td>
                                <td style="padding: 10px; border: 1px solid #ddd;">${budget:.2f}</td>
                            </tr>
            """
            
            if total_expenses > budget:
                over_budget = total_expenses - budget
                html_content += f"""
                            <tr style="background-color: #ffebee;">
                                <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold; color: #c62828;">Over Budget By:</td>
                                <td style="padding: 10px; border: 1px solid #ddd; color: #c62828; font-weight: bold;">${over_budget:.2f}</td>
                            </tr>
                """
        
        html_content += """
                        </table>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <p style="color: #666; font-size: 14px; margin: 0;">
                            This is an automated message from your ExpenseTracker system.<br>
                            Keep tracking your expenses for better financial insights!
                        </p>
                    </div>
                    
                    <div style="text-align: center; background: #f1f3f4; padding: 15px; border-radius: 8px;">
                        <p style="margin: 0; color: #555; font-size: 12px;">
                            📧 Weekly alerts: Every Sunday at 8:00 PM<br>
                            📊 Monthly reports: 1st of each month
                        </p>
                    </div>
                    
                </div>
            </div>
        </body>
        </html>
        """
        
        # Attach HTML content
        html_part = MIMEText(html_content, "html")
        msg.attach(html_part)
        
        # Send email (Use environment variable for production)
        EMAIL_ENABLED = os.environ.get('EMAIL_ENABLED', 'false').lower() == 'true'
        
        if EMAIL_ENABLED:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
            print(f"✅ {alert_type} email sent to {user_info.get('email')}")
        else:
            print(f"[EMAIL DISABLED] Would send {alert_type} to {user_info.get('email')}")
            print(f"Status: {status}")
            print(f"Total Expenses: ${total_expenses:.2f}")
            if budget > 0:
                print(f"Budget: ${budget:.2f}")
            
    except Exception as e:
        print(f"Error sending email: {e}")
