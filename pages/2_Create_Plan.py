import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime, timedelta, date
import matplotlib.pyplot as plt
from db import createPlan, getUserInfo, calculateUserAge, calculateGoalDate
from financial_plan import calculate_monthly_saving, handle_deletion, display_timeline, calculate_mortgage_payment, calculate_amortization_schedule, filter_models, calculate_car_savings, calculate_car_loan, calculate_pension_monthly_saving, calculate_loan
import time

def planning_page():
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        # Initialize session state for plans if not already set
        if 'plans' not in st.session_state:
            st.session_state['plans'] = []

        # --- PERSONAL INFORMATION ---
        # PREPARATION
        # Get user info
        user_id = st.session_state.user_id
        profile = getUserInfo(user_id)

        # Calculate birthday
        current_age = calculateUserAge(profile.user_birthday)

        # SHOW PLAN OPTIONS
        st.sidebar.title("Choose a plan")
        page = st.sidebar.selectbox("Go to", ["House Buyer Savings Plan", "Car Buyer Savings Plan", "Retirement Savings Plan", "Customized Financial Plan"])
        
        # SHOW PERSONAL INFORMATION
        st.sidebar.header(f'Your Personal Information')
        st.sidebar.number_input('Age', value = current_age)

        # Country selection
        country_data = {
            'Germany': {'Currency': '€', 'Inflation rate': 5.9, 'LifeExpectancy': 80.7},
            'United Kingdom': {'Currency': '£', 'Inflation rate': 6.8, 'LifeExpectancy': 82.1},
            'United States': {'Currency': '$', 'Inflation rate': 4.1, 'LifeExpectancy': 77.4}
        }

        selected_country = st.sidebar.selectbox('Country:', list(country_data.keys()), index=list(country_data.keys()).index(profile.user_country) if profile.user_country else 0)
        currency_symbol = country_data[selected_country]['Currency']
        inflation_rate = st.sidebar.slider('Annual inflation rate (%)', min_value=0.0, max_value=10.0, value=country_data[selected_country]['Inflation rate'], step=0.1, key='annual_inflation_rate')

        # Save life expectancy for later use
        life_expectancy = country_data[selected_country]['LifeExpectancy']

        # --- HOUSE BUYER SAVINGS PLAN ---
        if page == "House Buyer Savings Plan":
            st.title("House Buyer Savings Plan")

            goal_name = st.text_input("Name of the plan", value = "Buy a House")
            option = st.radio("Select Option", ["Savings Plan", "Mortgage Calculator"])
            house_price = st.number_input(f'House price ({currency_symbol}):', min_value=0.0, format="%.2f", key='house_price', value=250000.00)
            down_payment_percent = st.slider('Down payment percentage:', min_value=0.0, max_value=100.0, step=0.1, format="%.1f", key='down_payment_percent', value=10.00)
            target_age = st.number_input("Enter the age by which you want to achieve this goal:", min_value=current_age + 1, max_value=100, step=1, key='target_age')
            current_savings = st.number_input(f'Current savings for the house ({currency_symbol}, optional):', min_value=0.0, format="%.2f", key='current_savings')
            current_savings_return = 0
            if current_savings > 0:
                current_savings_return = st.slider('Annual return on current savings (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='current_savings_return')

            due_date = calculateGoalDate(profile.user_birthday, target_age)
            current_date = datetime.now().date()
            down_payment_amount = house_price * (down_payment_percent / 100)     
            # Placeholder todo
            payment_last_percent = 0
            payment_last = house_price * (payment_last_percent / 100) 
            # Calculate monthly saving
            savings_term_months = (due_date.year - current_date.year) * 12 + (due_date.month - current_date.month)
            monthly_saving = calculate_monthly_saving(house_price * (down_payment_percent / 100), current_savings, current_savings_return, savings_term_months, inflation_rate)            
              
            # SAVING PLAN OPTION 
            if option == "Savings Plan":
                if st.button('Calculate House Buyer Saving Plan'):  
                    # Save plan to DB
                    createPlan(user_id, goal_name, target_age, due_date, 
                                house_price, down_payment_amount, monthly_saving, 
                                current_savings, current_savings_return, savings_term_months,
                                down_payment_percent, down_payment_amount, payment_last_percent, payment_last, 
                                0, '1900-01-01', 0, 0, 0)
                    
                    # Write result
                    st.success("Plan created!")
                    time.sleep(0.8)
                    st.switch_page("Goaldigger.py")


            if option == "Mortgage Calculator":
                loan_amount = st.number_input(f'Mortgage loan amount ({currency_symbol}):', min_value=0.0, format="%.2f", value=0.0 if house_price == 0 else house_price - down_payment_amount - current_savings)
                loan_interest_rate = st.slider('Mortgage interest rate (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='loan_interest_rate')
                loan_term_years = st.number_input('Mortgage loan term (years):', min_value=1, max_value=50, step=1, key='loan_term_years')
                loan_start_date = st.date_input("Mortgage start date:", min_value=date.today(), key='loan_start_date', format="DD.MM.YYYY")  

                if st.button('Calculate Mortgage Payment'):
                    monthly_loan_payment, loan_amount = calculate_mortgage_payment(loan_amount, loan_interest_rate, loan_term_years)

                    # Add plan to database
                    createPlan(user_id, goal_name, target_age, due_date, 
                                house_price, down_payment_amount, monthly_saving, 
                                current_savings, current_savings_return, savings_term_months,
                                down_payment_percent, down_payment_amount, payment_last_percent, payment_last, 
                                loan_term_years, loan_start_date, loan_amount, loan_interest_rate, monthly_loan_payment)
                    
                    # Write result
                    st.success("Plan created!")
                    time.sleep(0.8)
                    st.switch_page("Goaldigger.py")

        # --- CAR BUYER SAVINGS PLAN ----
        if page == "Car Buyer Savings Plan":
            st.title("Car Buyer Savings Plan")
            # Enter goal name
            goal_name = st.text_input("Name of the plan", value = "Buy a Car")
            # Calculator option
            option = st.radio("Select Option", ["Savings Plan", "Car Loan Calculator"])

            #@st.cache_data
            df = pd.read_excel("data/car_prices.xlsx")

            if option == "Savings Plan":
                st.subheader('Choose an Option:')
                savings_option = st.radio('', ('See Available Suggested Car Prices', 'Input Your Car Price'))

                if savings_option == 'See Available Suggested Car Prices':
                    st.subheader('See Available Suggested Car Prices')

                    selected_make = st.selectbox('Select Car Brand', df['make'].unique())

                    if selected_make:
                        models = filter_models(df, selected_make)
                        selected_model = st.selectbox('Select Car Model', models)

                        if selected_model:
                            selected_car_details = df[(df['make'] == selected_make) & (df['model'] == selected_model)]
                            full_name = selected_car_details['make'].values[0] + ' ' + selected_car_details['model'].values[0]
                            price = selected_car_details['sellingprice'].values[0]
                            st.write(f"Full Name: {full_name}")
                            st.write(f"Suggested price: {currency_symbol}{price:.2f}")
                            # Option to input the price
                            car_price_input = st.number_input('Adjust the car price if needed:', min_value=0.0, format="%.2f", value=float(price), key='car_price_input')
                            
                                    

                elif savings_option == 'Input Your Car Price':
                    st.subheader('Input Your Car Price')
                    car_price_input = st.number_input('Enter the total cost of the car:', value=0.0, min_value=0.0, step=1000.0, format="%.2f")
                
                down_payment_percent = st.slider('Enter your down payment percentage:', min_value=0.0, max_value=100.0, step=1.0, key='car_down_payment_percent')
                down_payment_amount = car_price_input * (down_payment_percent / 100) 
                # Placeholder todo
                payment_last_percent = 0
                payment_last = car_price_input * (payment_last_percent / 100) 
                # Calculate age and date
                target_age = st.number_input('Enter the age you wish to buy the car:', value=30, min_value=current_age + 1, max_value=100, step=1, key='car_target_age')
                due_date = calculateGoalDate(profile.user_birthday, target_age)
                savings_term_months = (target_age - current_age) * 12
                current_savings = st.number_input(f'Current savings for the car ({currency_symbol}, optional):', min_value=0.0, format="%.2f", key='current_savings')
                # Option to enter savings return
                current_savings_return = 0
                if current_savings > 0:
                    current_savings_return = st.slider('Annual return on current savings (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='current_savings_return')

                # Calculate monthly saving
                monthly_saving = calculate_car_savings(car_price_input, down_payment_percent, current_age, target_age, current_savings, current_savings_return, inflation_rate)

                if st.button('Calculate Car Plan'):
                    # Save plan to DB
                    createPlan(user_id, goal_name, target_age, due_date, 
                                car_price_input, down_payment_amount, monthly_saving, 
                                current_savings, current_savings_return, savings_term_months,
                                down_payment_percent, down_payment_amount, payment_last_percent, payment_last, 
                                0, '1900-01-01', 0, 0, 0)
                    
                    # Write result
                    st.success("Plan created!")
                    time.sleep(0.8)
                    st.switch_page("Goaldigger.py")
                        
            if option == "Car Loan Calculator":
                st.subheader("Car Loan Calculator")

                car_price_input = st.number_input(f'Car price ({currency_symbol}):', min_value=0.0, format="%.2f", value=0.0, key='car_price_input')
                down_payment_percent = st.slider('Enter your down payment percentage:', min_value=0.0, max_value=100.0, step=1.0, key='car_down_payment_percent')
                down_payment_amount = car_price_input * (down_payment_percent / 100) 
                # Placeholder todo
                payment_last_percent = 0
                payment_last = car_price_input * (payment_last_percent / 100) 
                # Calculate age and date
                target_age = st.number_input('Enter the age you wish to buy the car:', value=30, min_value=current_age + 1, max_value=100, step=1, key='car_target_age')
                due_date = calculateGoalDate(profile.user_birthday, target_age)
                savings_term_months = (target_age - current_age) * 12
                current_savings = st.number_input(f'Current savings for the car ({currency_symbol}, optional):', min_value=0.0, format="%.2f", key='current_savings')
                # Option to enter savings return
                current_savings_return = 0
                if current_savings > 0:
                    current_savings_return = st.slider('Annual return on current savings (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='current_savings_return')

                # Calculate monthly saving
                monthly_saving = calculate_car_savings(car_price_input, down_payment_percent, current_age, target_age, current_savings, current_savings_return, inflation_rate)

                loan_amount = st.number_input(f'Loan amount ({currency_symbol}):', min_value=0.0, format="%.2f", value=0.0 if car_price_input == 0 else car_price_input - down_payment_amount - current_savings)
                loan_interest_rate = st.slider('Loan interest rate (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='car_loan_interest_rate')
                loan_term_years = st.number_input('Loan term (years):', value=2, min_value=0, max_value=30, step=1, key='car_loan_term_years')
                loan_start_date = st.date_input("Loan start date:", min_value=date.today(), key='car_loan_start_date')

                if st.button('Calculate Loan Payment'):
                    monthly_loan_payment, total_loan_payment = calculate_car_loan(loan_amount, loan_interest_rate, loan_term_years)
                    # Add plan to database
                    createPlan(user_id, goal_name, target_age, due_date, 
                                car_price_input, down_payment_amount, monthly_saving, 
                                current_savings, current_savings_return, savings_term_months,
                                down_payment_percent, down_payment_amount, payment_last_percent, payment_last, 
                                loan_term_years, loan_start_date, loan_amount, loan_interest_rate, monthly_loan_payment)
                    
                    # Write result
                    st.success("Plan created!")
                    time.sleep(0.8)
                    st.switch_page("Goaldigger.py")


        # --- RETIREMENT SAVINGS PLAN ----
        if page == "Retirement Savings Plan":
            st.title('Retirement Savings Plan')
            retirement_age = st.number_input('When do you want to retire?', min_value=current_age + 1, max_value=100, value=67, key='retirement_age')
            amount_needed = st.number_input(f'How much do you need at retirement (today\'s value, {currency_symbol})?', min_value=0.0, value=600000.0, key='pension_amount_needed')
            current_savings = st.number_input(f'Current retirement savings ({currency_symbol}):', min_value=0.0, value=30000.0, key='pension_current_savings')

            pension_current_savings_return = 0
            if current_savings > 0:
                pension_current_savings_return = st.slider('Annual return on current savings (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='pension_current_savings_return')

            if st.button('Calculate Retirement Plan'):
                pension_target_date = datetime.now().replace(year=datetime.now().year + (retirement_age - current_age))
                current_date = datetime.now().date()
                savings_term_years = retirement_age - current_age
                monthly_saving = calculate_pension_monthly_saving(amount_needed, current_savings, pension_current_savings_return, savings_term_years)
                
                plan = {
                    "name": "Retirement Savings Plan",
                    "down_payment_amount": amount_needed,
                    "due_date": pension_target_date,
                    "monthly_saving": monthly_saving,
                    "savings_term_months": savings_term_years * 12,
                    "details_link": "Retirement Savings Plan"
                }
                for idx, p in enumerate(st.session_state['plans']):
                    if p['name'] == "Retirement Savings Plan":
                        st.session_state['plans'][idx] = plan
                        break
                else:
                    st.session_state['plans'].append(plan)
                
                st.write(f"**Plan Name:** Retirement Savings Plan")
                st.write(f"**Target Amount:** {currency_symbol}{amount_needed:,.2f}")
                st.write(f"**Monthly Savings Needed:** <span style='color: red;'>{currency_symbol}{monthly_saving:,.2f}</span>", unsafe_allow_html=True)
                st.write(f"**Savings Term:** {savings_term_years} years")

        # --- CUSTOMIZED FINANCIAL PLAN ---
        if page == "Customized Financial Plan":
            st.title("Customized Financial Plan")

            # Inputs for custom financial plan
            plan_name = st.text_input("Enter the name of your plan:")
            plan_down_payment_amount = st.number_input(f"Enter the target amount ({currency_symbol}):", min_value=0.0, format="%.2f")
            plan_target_date = st.date_input("Enter the date by which you want to achieve this plan:")
            plan_current_savings = st.number_input(f"Enter your current savings for this plan ({currency_symbol}, optional):", min_value=0.0, format="%.2f")

            plan_current_savings_return = 0
            if plan_current_savings > 0:
                plan_current_savings_return = st.slider('Annual return on current savings (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f")

            loan_option = st.radio("Do you want to take a loan to cover this goal?", ("No", "Yes"))
            loan_amount = 0
            loan_term = 0
            loan_interest_rate = 0
            loan_start_date = None
            if loan_option == "Yes":
                loan_amount = st.number_input(f'Loan amount ({currency_symbol}):', min_value=0.0, format="%.2f")
                loan_term = st.number_input('Loan term (years):', min_value=1, max_value=30, step=1)
                loan_interest_rate = st.slider('Loan interest rate (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f")
                loan_start_date = st.date_input("Loan start date:", min_value=date.today())

            if st.button('Calculate Custom Plan'):
                current_date = datetime.now().date()
                if plan_target_date <= current_date:
                    st.error("Target date must be in the future.")
                else:
                    savings_term_months = (plan_target_date.year - current_date.year) * 12 + (plan_target_date.month - current_date.month)
                    if loan_option == "Yes":
                        adjusted_down_payment_amount = plan_down_payment_amount - loan_amount
                    else:
                        adjusted_down_payment_amount = plan_down_payment_amount
                    monthly_saving = calculate_monthly_saving(adjusted_down_payment_amount, plan_current_savings, plan_current_savings_return, savings_term_months, inflation_rate)
                    
                    plan = {
                        "name": plan_name,
                        "down_payment_amount": plan_down_payment_amount,
                        "due_date": plan_target_date,
                        "monthly_saving": monthly_saving,
                        "savings_term_months": savings_term_months,
                        "details_link": "Customized Financial Plan"
                    }
                    if loan_option == "Yes":
                        plan['loan_amount'] = loan_amount
                        plan['loan_term'] = loan_term
                        plan['loan_interest_rate'] = loan_interest_rate
                        plan['loan_start_date'] = loan_start_date
                        monthly_loan_payment, total_loan_payment = calculate_loan(loan_amount, loan_interest_rate, loan_term)
                        plan['monthly_loan_payment'] = monthly_loan_payment
                        plan['total_loan_payment'] = total_loan_payment
                        plan['custom_loan_end_date'] = loan_start_date + pd.DateOffset(years=loan_term)

                    #Check if a plan with the same name already exists and update it
                    for idx, p in enumerate(st.session_state['plans']):
                        if p['name'] == plan_name:
                            st.session_state['plans'][idx] = plan
                            break
                    else:
                        st.session_state['plans'].append(plan)
                    
                    st.write(f"**Plan Name:** {plan_name}")
                    st.write(f"**Target Amount:** {currency_symbol}{plan_down_payment_amount:,.2f}")
                    st.write(f"**Monthly Savings Needed:** <span style='color: red;'>{currency_symbol}{monthly_saving:,.2f}</span>", unsafe_allow_html=True)
                    st.write(f"**Savings Term:** {savings_term_months} months")

                    if loan_option == "Yes":
                        st.write(f"**Monthly Loan Payment:** {currency_symbol}{monthly_loan_payment:,.2f}")
                        st.write(f"**Total Loan Payment:** {currency_symbol}{total_loan_payment:,.2f}")

                        # Plot the amortization schedule
                        amortization_schedule = calculate_amortization_schedule(loan_amount, loan_interest_rate, loan_term, pd.Timestamp(loan_start_date))

                        fig = go.Figure()
                        fig.add_trace(go.Scatter(x=amortization_schedule['Month'], y=amortization_schedule['Payment'].cumsum(), mode='lines', name='Payment', line=dict(color='brown')))
                        fig.add_trace(go.Scatter(x=amortization_schedule['Month'], y=amortization_schedule['Interest'].cumsum(), mode='lines', name='Interest', line=dict(color='green')))
                        fig.add_trace(go.Scatter(x=amortization_schedule['Month'], y=amortization_schedule['Balance'], mode='lines', name='Balance', line=dict(color='blue')))
                        fig.update_layout(
                            title=f'Loan Amortization Schedule for {plan_name}',
                            xaxis_title='Year',
                            yaxis_title=f'Amount ({currency_symbol})',
                            xaxis=dict(tickmode='linear', tick0=0, dtick=12),
                            showlegend=True
                        )
                        st.plotly_chart(fig)

    else:
        st.warning("Please log in to access this page.")
        st.stop()

if __name__ == "__main__":
    planning_page()