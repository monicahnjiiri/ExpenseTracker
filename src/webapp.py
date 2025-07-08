import os
import sqlite3
import pandas as pd
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import json

# Import your existing modules (simplified for multi-user)
from .email_service import send_email_alert

app = Flask(__name__, template_folder='templates')
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')  # Use environment variable in production

# Database setup
def init_db():
    """Initialize the database with user and transaction tables"""
    conn = sqlite3.connect('expensetracker.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            budget REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Income table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL NOT NULL,
            source TEXT NOT NULL,
            description TEXT,
            date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Home page - login or dashboard if logged in"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        budget = float(request.form.get('budget', 0))
        
        # Hash password
        password_hash = generate_password_hash(password)
        
        try:
            conn = sqlite3.connect('expensetracker.db')
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (email, password_hash, name, budget) VALUES (?, ?, ?, ?)',
                (email, password_hash, name, budget)
            )
            conn.commit()
            conn.close()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
            
        except sqlite3.IntegrityError:
            flash('Email already exists!', 'error')
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect('expensetracker.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, password_hash, name FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['user_email'] = email
            session['user_name'] = user[2]
            flash(f'Welcome back, {user[2]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'error')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    """User dashboard with financial summary"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    # Get user's financial data
    conn = sqlite3.connect('expensetracker.db')
    
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
    
    # Get user budget
    cursor = conn.cursor()
    cursor.execute('SELECT budget FROM users WHERE id = ?', (user_id,))
    budget = cursor.fetchone()[0]
    conn.close()
    
    # Calculate totals
    total_expenses = expenses_df['amount'].sum() if not expenses_df.empty else 0
    total_income = income_df['amount'].sum() if not income_df.empty else 0
    savings = total_income - total_expenses
    
    # Recent transactions (last 10)
    recent_expenses = expenses_df.head(10).to_dict('records') if not expenses_df.empty else []
    recent_income = income_df.head(10).to_dict('records') if not income_df.empty else []
    
    return render_template('dashboard.html',
                         total_expenses=total_expenses,
                         total_income=total_income,
                         savings=savings,
                         budget=budget,
                         recent_expenses=recent_expenses,
                         recent_income=recent_income)

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    """Add new expense"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        user_id = session['user_id']
        amount = float(request.form['amount'])
        category = request.form['category']
        description = request.form.get('description', '')
        date = request.form['date']
        
        conn = sqlite3.connect('expensetracker.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)',
            (user_id, amount, category, description, date)
        )
        conn.commit()
        conn.close()
        
        flash(f'Expense of ${amount:.2f} added successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_expense.html')

@app.route('/add_income', methods=['GET', 'POST'])
def add_income():
    """Add new income"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        user_id = session['user_id']
        amount = float(request.form['amount'])
        source = request.form['source']
        description = request.form.get('description', '')
        date = request.form['date']
        
        conn = sqlite3.connect('expensetracker.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO income (user_id, amount, source, description, date) VALUES (?, ?, ?, ?, ?)',
            (user_id, amount, source, description, date)
        )
        conn.commit()
        conn.close()
        
        flash(f'Income of ${amount:.2f} added successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_income.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """User settings"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        user_id = session['user_id']
        budget = float(request.form['budget'])
        
        conn = sqlite3.connect('expensetracker.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET budget = ? WHERE id = ?', (budget, user_id))
        conn.commit()
        conn.close()
        
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    # Get current settings
    conn = sqlite3.connect('expensetracker.db')
    cursor = conn.cursor()
    cursor.execute('SELECT budget FROM users WHERE id = ?', (session['user_id'],))
    budget = cursor.fetchone()[0]
    conn.close()
    
    return render_template('settings.html', budget=budget)
    
@app.route('/init-db')
def trigger_db_init():
    init_db()
    return "Database initialized successfully!"

if __name__ == '__main__':
    init_db()
    print(" ExpenseTracker Multi-User App Starting...")
    print("Open your browser to: http://localhost:5000")
    app.run(debug=True)
