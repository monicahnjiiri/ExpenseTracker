import pandas as pd
def manipulate_data(df_expenses, df_income, user_input):
    """
    Expense Data Columns:
    ['Date', 'Category', 'Amount', 'Description', 'Payment_Method', 'Vendor']

    Income Data Columns:
    ['Date', 'Amount', 'Source', 'Type', 'Notes']
    """
    if df_expenses.empty and df_income.empty:
        return "No data available to process."

    # Example: Calculate total weekly expenses
    if 'Amount' not in df_expenses.columns:
        return "Column 'Amount' not found in expense data."
    # calculate weekly expenses
    df_expenses['Date'] = pd.to_datetime(df_expenses['Date'], errors='coerce')
    df_expenses['Week'] = df_expenses['Date'].dt.isocalendar().week
    weekly_expenses = df_expenses.groupby('Week')['Amount'].sum()
    print(f"Weekly Expenses:\n{weekly_expenses}")

    #Compare weekly expenses with budget from user input
    weekly_budget = user_input.get('weekly_budget', 0)
    try:
        weekly_budget = float(weekly_budget)
    except (ValueError, TypeError):
        weekly_budget = 0
        print("Warning: Invalid weekly budget, using 0.")
    
    total_weekly_expenses = weekly_expenses.sum()
    if total_weekly_expenses > weekly_budget:
        print(f"Warning: Weekly expenses ({total_weekly_expenses:.2f}) exceed the budget ({weekly_budget:.2f}).")
    else:
        print(f"Weekly expenses ({total_weekly_expenses:.2f}) are within the budget ({weekly_budget:.2f}).")

    # Calculate Monthly income
    if 'Amount' not in df_income.columns:
        return "Column 'Amount' not found in income data."
    df_income['Date'] = pd.to_datetime(df_income['Date'], errors='coerce')
    df_income['Month'] = df_income['Date'].dt.to_period('M')
    monthly_income = df_income.groupby('Month')['Amount'].sum()
    total_monthly_income = monthly_income.sum()
    print(f"Total Monthly Income: {total_monthly_income:.2f}")
    if total_monthly_income <= 0:
        return "Total income is zero or negative, cannot calculate savings."
    
    #Calculate monthly savings
    if 'Date' not in df_expenses.columns or 'Amount' not in df_expenses.columns:
        return "Required columns not found in expense data."    
    df_expenses['Month'] = df_expenses['Date'].dt.to_period('M')
    monthly_expenses = df_expenses.groupby('Month')['Amount'].sum()
    monthly_savings = total_monthly_income - monthly_expenses.sum()
    print(f"Monthly Savings: {monthly_savings:.2f}")

    # Get user details for tax calculation
    tax_year = user_input.get('tax_year', '2023')
    tax_class = user_input.get('tax_class', 'I')
    religious_status = user_input.get('religious_status', 'None')
    
    tax_rate = 0.25  # Example tax rate, can be adjusted based on tax class and religious status
    total_taxable_income = total_monthly_income * 12  # Annual income
    tax_due = total_taxable_income * tax_rate   
    print(f"Estimated Tax Due for {tax_year}: {tax_due:.2f}")
    return {
        "weekly_expenses": weekly_expenses,
        "monthly_income": monthly_income,
        "monthly_savings": monthly_savings,
        "tax_due": tax_due,
        "total_expenses": total_weekly_expenses
    }
