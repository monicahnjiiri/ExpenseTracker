def get_user_details():
    print("Please provide your details:")
    name = input("Full Name: ").strip()
    email = input("Email: ").strip()
    annual_income = input("Annual Income : ").strip()
    weekly_budget = input("Weekly Budget: ").strip()
    marital_Status = input("Marital Status: ").strip()
    tax_class = input("Tax Class: ").strip()
    religious_status = input("Religious Status: ").strip()
    tax_year = input("Tax Year: ").strip()

    # Convert numeric inputs
    try:
        annual_income = float(annual_income) if annual_income else 0
    except ValueError:
        annual_income = 0
        
    try:
        weekly_budget = float(weekly_budget) if weekly_budget else 0
    except ValueError:
        weekly_budget = 0
    
    return {
        "name": name,
        "email": email,
        "annual_income": annual_income,
        "weekly_budget": weekly_budget,
        "budget": weekly_budget,  # Add budget key for send_result function
        "marital_status": marital_Status,
        "tax_class": tax_class,
        "religious_status": religious_status,
        "tax_year": tax_year
    }
