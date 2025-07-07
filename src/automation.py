import sqlite3
import pandas as pd
import schedule
import time
import threading
from datetime import datetime, timedelta
from .email_service import send_email_alert

def get_user_data(user_id):
    """Get user's financial data from database"""
    conn = sqlite3.connect('expensetracker.db')
    
    # Get user info
    cursor = conn.cursor()
    cursor.execute('SELECT email, name, budget FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return None, None, None
    
    user_info = {
        'email': user[0],
        'name': user[1],
        'budget': user[2]
    }
    
    # Get expenses
    expenses_df = pd.read_sql_query(
        'SELECT amount, category, description, date FROM expenses WHERE user_id = ? ORDER BY date DESC',
        conn, params=(user_id,)
    )
    
    # Get income
    income_df = pd.read_sql_query(
        'SELECT amount, source, description, date FROM income WHERE user_id = ? ORDER BY date DESC',
        conn, params=(user_id,)
    )
    
    conn.close()
    
    return user_info, expenses_df, income_df

def calculate_financial_summary(expenses_df, income_df):
    """Calculate financial summary from dataframes"""
    total_expenses = expenses_df['amount'].sum() if not expenses_df.empty else 0
    total_income = income_df['amount'].sum() if not income_df.empty else 0
    
    # Calculate weekly expenses (last 7 days)
    if not expenses_df.empty:
        expenses_df['date'] = pd.to_datetime(expenses_df['date'])
        week_ago = datetime.now() - timedelta(days=7)
        weekly_expenses = expenses_df[expenses_df['date'] >= week_ago]['amount'].sum()
    else:
        weekly_expenses = 0
    
    # Calculate monthly data (last 30 days)
    if not expenses_df.empty:
        month_ago = datetime.now() - timedelta(days=30)
        monthly_expenses = expenses_df[expenses_df['date'] >= month_ago]['amount'].sum()
    else:
        monthly_expenses = 0
    
    if not income_df.empty:
        income_df['date'] = pd.to_datetime(income_df['date'])
        month_ago = datetime.now() - timedelta(days=30)
        monthly_income = income_df[income_df['date'] >= month_ago]['amount'].sum()
    else:
        monthly_income = 0
    
    result = {
        'weekly_expenses': weekly_expenses,
        'monthly_expenses': monthly_expenses,
        'monthly_income': monthly_income,
        'monthly_savings': monthly_income - monthly_expenses,
        'total_expenses': total_expenses,
        'total_income': total_income
    }
    
    return result

def send_weekly_alerts():
    """Send weekly alerts to all users"""
    print(f"🔔 Running weekly alerts at {datetime.now()}")
    
    try:
        conn = sqlite3.connect('expensetracker.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users')
        user_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        for user_id in user_ids:
            try:
                user_info, expenses_df, income_df = get_user_data(user_id)
                if user_info:
                    result = calculate_financial_summary(expenses_df, income_df)
                    
                    # Send email alert
                    send_email_alert(
                        user_info, 
                        result, 
                        result['total_expenses'], 
                        user_info['budget'],
                        alert_type="Weekly Summary"
                    )
                    print(f"✅ Weekly alert sent to {user_info['email']}")
                    
            except Exception as e:
                print(f"Error sending weekly alert to user {user_id}: {e}")
                
    except Exception as e:
        print(f"Error in weekly alerts: {e}")

def send_monthly_reports():
    """Send monthly reports to all users"""
    print(f"📊 Running monthly reports at {datetime.now()}")
    
    try:
        conn = sqlite3.connect('expensetracker.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users')
        user_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        for user_id in user_ids:
            try:
                user_info, expenses_df, income_df = get_user_data(user_id)
                if user_info:
                    result = calculate_financial_summary(expenses_df, income_df)
                    
                    # Send email alert
                    send_email_alert(
                        user_info, 
                        result, 
                        result['total_expenses'], 
                        user_info['budget'],
                        alert_type="Monthly Report"
                    )
                    print(f"✅ Monthly report sent to {user_info['email']}")
                    
            except Exception as e:
                print(f"Error sending monthly report to user {user_id}: {e}")
                
    except Exception as e:
        print(f"Error in monthly reports: {e}")

def start_automation():
    """Start the automated alert system"""
    print("🚀 Starting ExpenseTracker automation system...")
    
    # Schedule weekly alerts (every Sunday at 8 PM)
    schedule.every().sunday.at("20:00").do(send_weekly_alerts)
    
    # Schedule monthly reports (1st of each month at 9 AM)
    schedule.every().day.at("09:00").do(lambda: send_monthly_reports() if datetime.now().day == 1 else None)
    
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    # Start scheduler in background thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    print("✅ Automation system started!")
    print("📧 Weekly alerts: Every Sunday at 8:00 PM")
    print("📊 Monthly reports: 1st of each month at 9:00 AM")
    
    return scheduler_thread

if __name__ == "__main__":
    # Start the automation system
    start_automation()
    
    # Keep the script running
    try:
        while True:
            time.sleep(3600)  # Sleep for 1 hour
    except KeyboardInterrupt:
        print("⏹️ Automation system stopped.")
