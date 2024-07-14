import streamlit as st
import pandas as pd
from datetime import datetime, date
from db import createPlan, getUserInfo, calculateUserAge, calculateGoalDate, calculateGoalAge, logout, showChosenPages
from financial_plan import calculate_monthly_saving, calculate_loan_payment, filter_models, calculate_car_savings, calculate_pension_monthly_saving
import time

showChosenPages()

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 加载 CSS 文件
css_file_path = "data/titlestyle.css"
load_css(css_file_path)

def planning_page():
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        logout()

        # --- PERSONAL INFORMATION ---
        # PREPARATION
        # Get user info
        user_id = st.session_state.user_id
        profile = getUserInfo(user_id)

        # Calculate birthday
        current_age = calculateUserAge(profile.user_birthday)
        current_date = datetime.now().date()

        # SHOW PLAN OPTIONS
        st.sidebar.title("Choose a plan")
        page = st.sidebar.radio("Go to 👉", ["🏡 House Buyer Savings Plan", "🚘 Car Buyer Savings Plan", "👵🏼 Retirement Savings Plan", "🔧 Customized Financial Plan"])
        
        # SHOW PERSONAL INFORMATION
        st.sidebar.header(f'📝 Your Personal Information')
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
        if page == "🏡 House Buyer Savings Plan":
            st.markdown(
                f"""
                <h1>🏡 House Buyer Savings Plan</h1>
                """,
                unsafe_allow_html=True
            )
            st.divider()
            goal_type = "House Buyer Savings Plan"
            goal_name = st.text_input("Name of the plan", value = "Buy a House")
            house_price = st.number_input(f'House price ({currency_symbol}):', min_value=0.0, format="%.2f", key='house_price', value=250000.00)
            down_payment_percent = st.slider('Down payment percentage:', min_value=0.0, max_value=100.0, step=0.1, format="%.1f", key='down_payment_percent', value=10.00)
            target_age = st.number_input("Enter the age by which you want to achieve this goal:", min_value=current_age + 1, max_value=100, step=1, key='target_age')
            current_savings = st.number_input(f'Current savings for the house ({currency_symbol}, optional):', min_value=0.0, format="%.2f", key='current_savings')
            current_savings_return = 0
            if current_savings > 0:
                current_savings_return = st.slider('Annual return on current savings (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='current_savings_return')

            due_date = calculateGoalDate(profile.user_birthday, target_age)
            
            down_payment_amount = house_price * (down_payment_percent / 100)     
            # Placeholder todo
            payment_last_percent = 0
            payment_last = house_price * (payment_last_percent / 100) 
            # Calculate monthly saving
            savings_term_months = (due_date.year - current_date.year) * 12 + (due_date.month - current_date.month)
            monthly_saving = calculate_monthly_saving(house_price * (down_payment_percent / 100), current_savings, current_savings_return, savings_term_months, inflation_rate)   

            take_house_loan = st.radio("Do you want to take a mortgage loan?", ("Yes", "No"), index=1)
            if take_house_loan == "Yes":
                loan_amount = st.number_input(f'Mortgage loan amount ({currency_symbol}):', min_value=0.0, format="%.2f", value=0.0 if take_house_loan == "No" else house_price - down_payment_amount - current_savings)
                loan_interest_rate = st.slider('Mortgage interest rate (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='loan_interest_rate', value=0.0 if take_house_loan == "No" else 5.7)
                loan_term_years = st.number_input('Mortgage loan term (years):', min_value=1, max_value=50, step=1, key='loan_term_years', value=0 if take_house_loan == "No" else 20)
                loan_start_date = st.date_input("Mortgage start date:", min_value=date.today(), key='loan_start_date', format="DD.MM.YYYY", value="01.01.1900" if take_house_loan == "No" else current_date)  
                monthly_loan_payment = calculate_loan_payment(loan_amount, loan_interest_rate, loan_term_years)
            else:
                loan_amount = 0.0
                loan_interest_rate = 0.0
                loan_term_years = 0
                loan_start_date = date.today()
                monthly_loan_payment = 0.0

              
            # SAVING PLAN OPTION 
            if st.button('Calculate House Buyer Saving Plan'):  
                # Add plan to database
                plan_id = createPlan(user_id, goal_type, goal_name, target_age, due_date, 
                            house_price, down_payment_amount, monthly_saving, 
                            current_savings, current_savings_return, savings_term_months,
                            down_payment_percent, down_payment_amount, payment_last_percent, payment_last, 
                            loan_term_years, loan_start_date, loan_amount, loan_interest_rate, monthly_loan_payment)
                
                # Write result
                st.success("Plan created!")
                time.sleep(0.8)
                # Save the plan_id in session
                st.session_state.edit_plan_id = plan_id                
                st.switch_page("pages/3_Edit_Plan.py")

        # --- CAR BUYER SAVINGS PLAN ----
        if page == "🚘 Car Buyer Savings Plan":
            st.markdown(
                f"""
                <h1>🚘 Car Buyer Savings Plan</h1>
                """,
                unsafe_allow_html=True
            )
            st.divider()
            goal_type = "Car Buyer Savings Plan"
            # Enter goal name
            goal_name = st.text_input("Name of the plan", value = "Buy a Car")
            df = pd.read_excel("data/car_prices.xlsx")

            st.subheader('Choose an Option 👉:')
            savings_option = st.radio('', ('See Available Suggested Car Prices', 'Input Your Car Price'))

            if savings_option == 'See Available Suggested Car Prices':
                st.subheader('See Available Suggested Car Prices')

                col1, col2, col3 = st.columns(3)
                selected_make = col1.selectbox('Select Car Make', df['make'].unique())
                selected_model = None

                if selected_make:
                    models = filter_models(df, selected_make)
                    selected_model = col2.selectbox('Select Car Model', models)

                    if selected_model:
                        selected_car_details = df[(df['make'] == selected_make) & (df['model'] == selected_model)]
                        price = selected_car_details['sellingprice'].values[0]
                        col3.write(f"Suggested price: {currency_symbol}{price:.2f}")

                car_price_input = st.number_input('Adjust the car price if needed:', min_value=0.0, format="%.2f", value=float(price) if selected_model else 0.0, key='adjusted_car_price')
            else:
                st.subheader('Input Your Car Price')
                car_price_input = st.number_input('Enter the total cost of the car:', min_value=0.0, format="%.2f", key='adjusted_car_price')
                
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

            take_car_loan = st.radio("Do you want to take a car loan?", ("Yes", "No"), index=1)
            if take_car_loan == "Yes":
                loan_amount = st.number_input(f'Car loan amount ({currency_symbol}):', min_value=0.0, format="%.2f", value=0.0 if take_car_loan == "No" else car_price_input - down_payment_amount - current_savings)
                loan_interest_rate = st.slider('Car interest rate (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='loan_interest_rate', value=0.0 if take_car_loan == "No" else 5.7)
                loan_term_years = st.number_input('Car loan term (years):', min_value=1, max_value=50, step=1, key='loan_term_years', value=0 if take_car_loan == "No" else 2)
                loan_start_date = st.date_input("Car start date:", min_value=date.today(), key='loan_start_date', format="DD.MM.YYYY", value="01.01.1900" if take_car_loan == "No" else current_date)  
                monthly_loan_payment = calculate_loan_payment(loan_amount, loan_interest_rate, loan_term_years)
            else:
                loan_amount = 0.0
                loan_interest_rate = 0.0
                loan_term_years = 0
                loan_start_date = date.today()
                monthly_loan_payment = 0.0

            if st.button('Calculate Car Plan'):
                # Save plan to DB
                plan_id = createPlan(user_id, goal_type, goal_name, target_age, due_date, 
                            car_price_input, down_payment_amount, monthly_saving, 
                            current_savings, current_savings_return, savings_term_months,
                            down_payment_percent, down_payment_amount, payment_last_percent, payment_last, 
                            loan_term_years, loan_start_date, loan_amount, loan_interest_rate, monthly_loan_payment)
                
                # Write result
                st.success("Plan created!")
                time.sleep(0.8)
                # Save the plan_id in session
                st.session_state.edit_plan_id = plan_id                
                st.switch_page("pages/3_Edit_Plan.py")


        # --- RETIREMENT SAVINGS PLAN ----
        if page == "👵🏼 Retirement Savings Plan":
            st.markdown(
                f"""
                <h1>👵🏼 Retirement Savings Plan</h1>
                """,
                unsafe_allow_html=True
            )
            st.divider()
            goal_type = "Retirement Savings Plan"

            # Enter goal name
            goal_name = st.text_input("Name of the plan", value = "Retirement Savings Plan")
            target_age = st.number_input('When do you want to retire?', min_value=current_age + 1, max_value=100, value=67, key='target_age')
            retirement_amount = st.number_input(f'How much do you need at retirement (today\'s value, {currency_symbol})?', min_value=0.0, value=600000.0, key='pension_down_payment_amount')
            current_savings = st.number_input(f'Current retirement savings ({currency_symbol}):', min_value=0.0, value=30000.0, key='pension_current_savings')
            # Option to enter current savings return
            current_savings_return = 0
            if current_savings > 0:
                current_savings_return = st.slider('Annual return on current savings (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='current_savings_return')
                
            due_date = calculateGoalDate(profile.user_birthday, target_age)
            
            savings_term_months = (target_age - current_age) * 12
            monthly_saving = calculate_pension_monthly_saving(retirement_amount, current_savings, current_savings_return, savings_term_months)

            if st.button('Calculate Retirement Plan'):
                # Save plan to DB
                plan_id = createPlan(user_id, goal_type, goal_name, target_age, due_date, 
                            retirement_amount, retirement_amount, monthly_saving, 
                            current_savings, current_savings_return, savings_term_months,
                            0, savings_term_months, 0, 0, 
                            0, '1900-01-01', 0, 0, 0)
                
                # Write result
                st.success("Plan created!")
                time.sleep(0.8)
                # Save the plan_id in session
                st.session_state.edit_plan_id = plan_id                
                st.switch_page("pages/3_Edit_Plan.py")

        # --- CUSTOMIZED FINANCIAL PLAN ---
        if page == "🔧 Customized Financial Plan":
            st.markdown(
                f"""
                <h1>🔧 Customized Financial Plan</h1>
                """,
                unsafe_allow_html=True
            )
            st.divider()
            goal_type = "Customized Financial Plan"

            # Inputs for custom financial plan
            goal_name = st.text_input("Enter the name of your plan:")
            goal_total = st.number_input(f"Enter the target amount ({currency_symbol}):", min_value=0.0, format="%.2f")
            down_payment_percent = st.slider('Enter your down payment percentage:', min_value=0.0, max_value=100.0, step=1.0, key='down_payment_percent')
            down_payment_amount = goal_total * (down_payment_percent / 100) 
            # Placeholder todo
            payment_last_percent = 0
            payment_last = goal_total * (payment_last_percent / 100) 
            due_date = st.date_input("Enter the date by which you want to achieve this plan:", format="DD.MM.YYYY", value=date.today())
            target_age = calculateGoalAge(profile.user_birthday, due_date)
            current_savings = st.number_input(f"Enter your current savings for this plan ({currency_symbol}, optional):", min_value=0.0, format="%.2f")
            # Option to enter saving returns
            current_savings_return = 0
            if current_savings > 0:
                current_savings_return = st.slider('Annual return on current savings (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f")

            # Option to take a loan
            loan_option = st.radio("Do you want to take a loan to cover this goal?", ("No", "Yes"))
            loan_amount = 0
            loan_term_years = 0
            loan_interest_rate = 0
            loan_start_date = None
            if loan_option == "Yes":
                loan_amount = st.number_input(f'Loan amount ({currency_symbol}):', min_value=0.0, format="%.2f", value=0.0 if goal_total == 0 else goal_total - down_payment_amount - current_savings)
                loan_term_years = st.number_input('Loan term (years):', min_value=1, max_value=30, step=1)
                loan_interest_rate = st.slider('Loan interest rate (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f")
                loan_start_date = st.date_input("Loan start date:", value=date.today(), format="DD.MM.YYYY")
                monthly_loan_payment = calculate_loan_payment(loan_amount, loan_interest_rate, loan_term_years)

                savings_term_months = (due_date.year - current_date.year) * 12 + (due_date.month - current_date.month)
                if down_payment_amount > 0:
                    goal_target = down_payment_amount - current_savings
                else:
                    goal_target = goal_total - current_savings
                monthly_saving = calculate_monthly_saving(goal_target, current_savings, current_savings_return, savings_term_months, inflation_rate)


            if st.button('Calculate Custom Plan'):
                # Add plan to database
                plan_id = createPlan(user_id, goal_type, goal_name, target_age, due_date, 
                            goal_total, down_payment_amount, monthly_saving, 
                            current_savings, current_savings_return, savings_term_months,
                            down_payment_percent, down_payment_amount, payment_last_percent, payment_last, 
                            loan_term_years, loan_start_date, loan_amount, loan_interest_rate, monthly_loan_payment)
                
                # Write result
                st.success("Plan created!")
                time.sleep(0.8)
                # Save the plan_id in session
                st.session_state.edit_plan_id = plan_id                
                st.switch_page("pages/3_Edit_Plan.py")

    else:
        st.warning("Please log in to access this page.")
        st.stop()

if __name__ == "__main__":
    planning_page()
