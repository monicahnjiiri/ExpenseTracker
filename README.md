# 💰 ExpenseTracker - Multi-User Web Application

A beautiful, automated expense tracking web application with multi-user support and email alerts.

## 🚀 Live Demo
Deploy this application to any cloud platform in minutes!

## ✨ Features
- 👥 **Multi-User Support** - Individual accounts for each user
- 📊 **Real-Time Dashboard** - Live financial metrics
- 📧 **Automated Alerts** - Weekly/monthly email summaries
- 💡 **Budget Warnings** - Smart overspend notifications
- 🔒 **Secure** - Password hashing and session management
- 📱 **Responsive Design** - Works on all devices

## 🏗️ Project Structure
```
ExpenseTracker/
├── src/                    # Source code
│   ├── webapp.py          # Flask web application
│   ├── automation.py      # Background email automation
│   ├── email_service.py   # Email functionality
│   └── templates/         # HTML templates
├── start_app.py           # Application launcher
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku deployment
├── runtime.txt           # Python version
└── .gitignore           # Git ignore rules
```

## 🚀 Quick Start

### Local Development
```bash
pip install -r requirements.txt
python start_app.py
```
Open: http://localhost:5000

### Deploy to Heroku
```bash
git init
git add .
git commit -m "Deploy ExpenseTracker"
heroku create your-app-name
git push heroku main
```

### Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Connect this GitHub repository
3. Deploy automatically!

## 📧 Email Configuration (Optional)
Set environment variables for automated email alerts:
```bash
# For Heroku
heroku config:set EMAIL_ENABLED=true
heroku config:set SENDER_EMAIL=your-email@gmail.com
heroku config:set SENDER_PASSWORD=your-gmail-app-password
```

## 🛠️ Technology Stack
- **Backend**: Python Flask
- **Database**: SQLite (upgradable to PostgreSQL)
- **Frontend**: HTML/CSS with responsive design
- **Email**: SMTP via Gmail
- **Automation**: Background scheduling
- **Deployment**: Cloud-ready with Heroku/Railway support

## 📱 User Features
1. **Register/Login** - Secure account creation
2. **Add Expenses** - Easy expense tracking with categories
3. **Add Income** - Income source management
4. **Dashboard** - Financial overview and recent transactions
5. **Settings** - Budget management and preferences
6. **Automated Reports** - Weekly and monthly email summaries

## 📊 Automated Schedule
- **Weekly Alerts**: Every Sunday at 8:00 PM
- **Monthly Reports**: 1st of each month at 9:00 AM

## 🎯 Perfect For
- Personal finance tracking
- Small business expense management
- Portfolio projects
- Learning Flask development
- Demonstrating full-stack skills

---

🎉 **Ready to deploy and share with the world!** 🌐