import streamlit as st
import numpy as np
import numpy_financial as npf
from datetime import datetime, timedelta, date

### FINANCIAL LOGIC ###

# Helper function to calculate monthly savings
def calculate_monthly_saving(target_amount, current_savings, current_savings_return, savings_term_months, inflation_rate):
    # Adjust the target amount for inflation
    if target_amount > 0:
        future_value_target_amount = target_amount * ((1 + inflation_rate / 100) ** (savings_term_months / 12))

        monthly_interest_rate = current_savings_return / 100 / 12
        number_of_payments = savings_term_months

        if current_savings > 0:
            current_savings_future_value = current_savings * ((1 + monthly_interest_rate) ** number_of_payments)
            future_value_needed = future_value_target_amount - current_savings_future_value
        else:
            future_value_needed = future_value_target_amount

        if future_value_needed <= 0:
            return 0, float(round(future_value_target_amount, 2))

        # Avoid division by zero or negative rates
        if monthly_interest_rate == 0:
            if number_of_payments == 0:
                # todo
                number_of_payments = 3
            monthly_saving = future_value_needed / number_of_payments
        else:
            try:
                monthly_saving = npf.pmt(monthly_interest_rate, number_of_payments, 0, -future_value_needed)
            except (ValueError, OverflowError) as e:
                print(f"Error calculating monthly saving: {e}")
                return float('inf'), float(round(future_value_target_amount, 2))
    else:
        monthly_saving = 0
        future_value_needed = 0
        future_value_target_amount = 0

    return float(round(monthly_saving, 2)), float(round(future_value_target_amount, 2))

def calculateMonthlyFinalPayment(final_payment_amount, loan_term_years):
    loan_term_months = loan_term_years * 12
    monthly_final_payment = final_payment_amount // loan_term_months if loan_term_years > 0 else 0
    return monthly_final_payment

def filter_models(df, selected_make):
    models = df[df['make'] == selected_make]['model'].unique()
    return models

# Calculate mortgage payment
def calculate_loan_payment(loan_amount, annual_interest_rate, loan_term_years):
    monthly_interest_rate = annual_interest_rate / 100 / 12
    number_of_payments = loan_term_years * 12
    monthly_payment = np.abs(npf.pmt(monthly_interest_rate, number_of_payments, loan_amount))
    total_payment = monthly_payment * number_of_payments
    return float(monthly_payment)

# Function to filter plans based on the selected date range
def filter_plans_by_date(plans, selected_month):
    filtered_plans = []
    for plan in plans:
        plan_due_date = plan.goal_date if isinstance(plan.goal_date, datetime) else datetime.combine(plan.goal_date, datetime.min.time())
        if plan_due_date >= selected_month:
            filtered_plans.append(plan)
    return filtered_plans
    
# Function to filter loans based on the selected date range
def filter_loans_by_date(plans, selected_month):
    total_monthly_loans = 0
    for plan in plans:
        if plan.goal_target_monthly:
            loan_start_date = plan.loan_startdate.date() if isinstance(plan.loan_startdate, datetime) else plan.loan_startdate
            loan_end_date = loan_start_date + timedelta(days=plan.loan_duration * 365)
            if loan_start_date <= selected_month.date() <= loan_end_date:
                total_monthly_loans += plan.loan_monthly
    return total_monthly_loans

### CALCULATIONS ###

# Calculate date function
def calculateGoalDate(user_birthday, goal_age):
    """
    Calculate the goal date by adding goal_age years to the user's birthday.
    """
    # Calculate the goal date
    goal_date = user_birthday + timedelta(days=goal_age * 365.25)  # Approximately accounts for leap years
    return goal_date

def calculateSavingDuration(goal_date):
    """
    Calculate the number of days from today until the goal date.
    """
    today = datetime.today()
    # Calculate the duration in days
    duration_days = (goal_date - today).days
    return duration_days

def calculateGoalAge(user_birthday, goal_date):
    """
    Calculate the goal age by subtracting goal_date from the user's birthday and get the lower number
    """
    # Calculate the difference in years
    goal_age = goal_date.year - user_birthday.year
    
    # Adjust for cases where the goal date is before the birthday in the year
    if (goal_date.month, goal_date.day) < (user_birthday.month, user_birthday.day):
        goal_age -= 1
    
    return goal_age

def calculateUserAge(user_birthday):
    """
    Calculate the user age by subtracting today from the user's birthday and get the lower number
    """
    # Calculate the difference in years
    today = date.today()
    user_age = today.year - user_birthday.year
    
    # Adjust for cases where the goal date is before the birthday in the year
    if (today.month, today.day) < (user_birthday.month, user_birthday.day):
        user_age -= 1
    
    return user_age