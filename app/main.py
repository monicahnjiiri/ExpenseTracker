import pandas as pd
from modules.fetch_csv import read_csv_data
from modules.user_input import get_user_details
from modules.process_data import manipulate_data
from modules.send_output import send_result, setup_automation

def main():
    # Step 1: Read data
    expense_data: pd.DataFrame = read_csv_data("data/Expenses.csv")
    print(f"Expense Data:\n{expense_data.columns.to_list()}")
    income_data: pd.DataFrame = read_csv_data("data/Income.csv")
    print(f"Income Data:\n{income_data.columns.to_list()}")

    # Step 2: Get user input
    user_info = get_user_details()
    print(f"User Info: {user_info}")

    # Step 3: Manipulate data
    result = manipulate_data(expense_data, income_data, user_info)

    # Step 4: Send results
    send_result(user_info, result)
    
    # Optional: Start automated alerts
    start_automation = input("\n🔔 Would you like to start automated weekly/monthly alerts? (y/n): ").strip().lower()
    if start_automation in ['y', 'yes']:
        scheduler_thread = setup_automation()
        if scheduler_thread:
            print("\n✅ Automation is now running!")
            print("📧 Weekly alerts: Every Sunday at 8:00 PM")
            print("📊 Monthly reports: 1st of each month")
            print("🔄 Just keep updating your CSV files daily!")
            print("\nPress Enter to exit (automation continues in background)...")
            input()

if __name__ == "__main__":
    main()
