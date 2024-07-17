import streamlit as st
import pandas as pd
from datetime import datetime, date
from db import createPlan, getUserInfo, logout, showChosenPages
from financial_plan import calculate_monthly_saving, calculate_loan_payment, filter_models, calculateMonthlyFinalPayment, calculateUserAge, calculateGoalDate
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
            goal_total = st.number_input(f'House price ({currency_symbol}):', min_value=0.0, format="%.2f", key='goal_total', value=250000.00)
            target_age = st.number_input("Enter the age by which you want to achieve this goal:", min_value=current_age + 1, max_value=100, step=1, key='target_age')
            due_date = calculateGoalDate(profile.user_birthday, target_age)

            # Current saving
            col1_1, col1_2 = st.columns([1, 3])
            with col1_1:
                current_savings = st.number_input(f'Current savings for the house ({currency_symbol}, optional):', min_value=0.0, format="%.2f", key='current_savings')
            if current_savings > 0:
                with col1_2:
                    current_savings_return = st.slider('Annual return on current savings (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='current_savings_return', value=1.6)
            else:
                current_savings_return = 0
        
            st.divider()

            # MORTGAGE LOAN
            col1_1, col1_2 = st.columns([2, 3])
            with col1_1:
                st.subheader('Choose an Option: 👉')
            with col1_2:
                loan_radio = st.radio("Do you want to calculate the mortgage loan?", ("Yes", "No"), index=1)
            
            if loan_radio == "Yes":
                st.divider()
                # Down payment
                col1_1, col1_2 = st.columns([1, 3])
                with col1_1:
                    down_payment_radio = st.radio("Is there a down payment?", ("Yes", "No"), index=0)
                if down_payment_radio == "Yes":
                    with col1_2:
                        down_payment_percent = st.slider('Down payment (%):', min_value=0.0, max_value=100.0, step=0.1, format="%.1f", key='down_payment_percent', value=10.00)
                        down_payment_amount = round(goal_total * (down_payment_percent / 100), 2)
                        st.write(f"👉 Down payment: {down_payment_amount:.2f} {profile.user_currency}")
                else:
                    down_payment_percent = 0.0
                    down_payment_amount = 0.0
                
                st.divider()
                
                # Final payment
                col1_1, col1_2 = st.columns([1, 3])
                with col1_1:
                    final_payment_radio = st.radio("Is there a final payment?", ("Yes", "No"), index=0)
                if final_payment_radio == "Yes":
                    with col1_2:
                        final_payment_percent = st.slider('Final payment (%):', min_value=0.0, max_value=100.0, step=0.1, format="%.1f", key='final_payment_percent', value=10.00)
                        final_payment_amount = round(goal_total * (final_payment_percent / 100), 2)  
                        st.write(f"👉 Final payment: {final_payment_amount:.2f} {profile.user_currency}")
                else:
                    final_payment_percent = 0.0
                    final_payment_amount = 0.0

                st.divider()
                loan_amount_input = goal_total - down_payment_amount - final_payment_amount if down_payment_amount > 0 else goal_total - current_savings
                # Loan rate
                col1_1, col1_2 = st.columns([1, 3])
                with col1_1:
                    loan_amount = st.number_input(f'Mortgage loan amount ({currency_symbol}):', min_value=0.0, format="%.2f", value=loan_amount_input)
                with col1_2:
                    loan_interest_rate = st.slider('Mortgage interest rate (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='loan_interest_rate', value=5.7)
                loan_term_years = st.number_input('Mortgage loan term (years):', min_value=0, max_value=50, step=1, key='loan_term_years', value=20)
                loan_start_date = st.date_input("Mortgage start date:", min_value=current_date, key='loan_start_date', format="DD.MM.YYYY", value=due_date)  
                monthly_loan_payment = calculate_loan_payment(loan_amount, loan_interest_rate, loan_term_years)
                goal_target = down_payment_amount - current_savings if down_payment_amount > 0 else goal_total - loan_amount
                
            else:
                down_payment_percent = 0.0
                down_payment_amount = 0.0
                final_payment_percent = 0.0
                final_payment_amount = 0.0
                loan_amount = 0.0
                loan_interest_rate = 0.0
                loan_term_years = 0
                loan_start_date = current_date
                monthly_loan_payment = 0.0
                goal_target = goal_total - current_savings
                down_payment_radio = None
                final_payment_radio = None

              
            # Calculate monthly saving
            savings_term_months = (due_date.year - current_date.year) * 12 + (due_date.month - current_date.month)
            monthly_final_payment = calculateMonthlyFinalPayment(final_payment_amount, loan_term_years)
            combined_monthly_payment = monthly_loan_payment + monthly_final_payment
            monthly_saving, future_goal_target = calculate_monthly_saving(goal_target, current_savings, current_savings_return, savings_term_months, inflation_rate)   

            st.divider()

            # SAVING PLAN OPTION 
            if st.button('Calculate House Buyer Saving Plan'):  
                # Add plan to database
                plan_id = createPlan(user_id, goal_type, goal_name, None, None, target_age, due_date, 
                            goal_total, goal_target, monthly_saving, 
                            current_savings, current_savings_return, savings_term_months,
                            loan_radio, down_payment_radio, final_payment_radio,
                            down_payment_percent, down_payment_amount, final_payment_percent, final_payment_amount, 
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
                selected_brand = col1.selectbox('Select Car Brand', df['make'].unique())
                selected_model = None

                if selected_brand:
                    models = filter_models(df, selected_brand)
                    selected_model = col2.selectbox('Select Car Model', models)

                    if selected_model:
                        selected_car_details = df[(df['make'] == selected_brand) & (df['model'] == selected_model)]
                        price = selected_car_details['sellingprice'].values[0]
                        col3.write(f"Suggested price: {price:.2f} {currency_symbol}")

                goal_total = st.number_input('Adjust the car price if needed:', min_value=0.0, format="%.2f", value=float(price) if selected_model else 0.0, key='adjusted_car_price')
            else:
                st.subheader('Input Your Car Price')
                goal_total = st.number_input('Enter the total cost of the car:', min_value=0.0, format="%.2f", key='adjusted_car_price')
            
            # Calculate age and date
            target_age = st.number_input('Enter the age you wish to buy the car:', min_value=current_age + 1, max_value=100, step=1, key='car_target_age')
            due_date = calculateGoalDate(profile.user_birthday, target_age)
            savings_term_months = (target_age - current_age) * 12
            
            # Current saving
            col1_1, col1_2 = st.columns([1, 3])
            with col1_1:
                current_savings = st.number_input(f'Current savings for the car ({currency_symbol}, optional):', min_value=0.0, format="%.2f", key='current_savings')
            if current_savings > 0:
                with col1_2:
                    current_savings_return = st.slider('Annual return on current savings (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='current_savings_return', value=1.6)
            else:
                current_savings_return = 0
            
            st.divider()

            # CAR LOAN
            col1_1, col1_2 = st.columns([2, 3])
            with col1_1:
                st.subheader('Choose an Option: 👉')
            with col1_2:
                loan_radio = st.radio("Do you want to calculate the car loan?", ("Yes", "No"), index=1)
            
            if loan_radio == "Yes":
                st.divider()

                # Down payment
                col1_1, col1_2 = st.columns([1, 3])
                with col1_1:
                    down_payment_radio = st.radio("Is there a down payment?", ("Yes", "No"), index=0)
                if down_payment_radio == "Yes":
                    with col1_2:
                        down_payment_percent = st.slider('Down payment (%):', min_value=0.0, max_value=100.0, step=0.1, format="%.1f", key='down_payment_percent', value=20.00)
                        down_payment_amount = round(goal_total * (down_payment_percent / 100), 2)
                        st.write(f"👉 Down payment: {down_payment_amount:.2f} {profile.user_currency}")
                else:
                    down_payment_percent = 0.0
                    down_payment_amount = 0.0
                
                st.divider()

                # Final payment
                col1_1, col1_2 = st.columns([1, 3])
                with col1_1:
                    final_payment_radio = st.radio("Is there a final payment?", ("Yes", "No"), index=0)
                if final_payment_radio == "Yes":
                    with col1_2:
                        final_payment_percent = st.slider('Final payment (%):', min_value=0.0, max_value=100.0, step=0.1, format="%.1f", key='final_payment_percent', value=40.00)
                        final_payment_amount = round(goal_total * (final_payment_percent / 100), 2)  
                        st.write(f"👉 Final payment: {final_payment_amount:.2f} {profile.user_currency}")
                else:
                    final_payment_percent = 0.0
                    final_payment_amount = 0.0

                st.divider()

                loan_amount_input = goal_total - down_payment_amount - final_payment_amount if down_payment_amount > 0 else goal_total - current_savings
                # Loan rate
                col1_1, col1_2 = st.columns([1, 3])
                with col1_1:
                    loan_amount = st.number_input(f'Car loan amount ({currency_symbol}):', min_value=0.0, format="%.2f", value=loan_amount_input)
                with col1_2:
                    loan_interest_rate = st.slider('Car interest rate (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='loan_interest_rate', value=5.7)
                loan_term_years = st.number_input('Car loan term (years):', min_value=0, max_value=50, step=1, key='loan_term_years', value=2)
                loan_start_date = st.date_input("Car loan start date:", min_value=current_date, key='loan_start_date', format="DD.MM.YYYY", value=due_date)  
                monthly_loan_payment = calculate_loan_payment(loan_amount, loan_interest_rate, loan_term_years)
                goal_target = down_payment_amount - current_savings if down_payment_amount > 0 else goal_total - loan_amount
                
            else:
                down_payment_percent = 0.0
                down_payment_amount = 0.0
                final_payment_percent = 0.0
                final_payment_amount = 0.0
                loan_amount = 0.0
                loan_interest_rate = 0.0
                loan_term_years = 0
                loan_start_date = current_date
                monthly_loan_payment = 0.0
                goal_target = goal_total - current_savings
                down_payment_radio = None
                final_payment_radio = None

            # Calculate monthly saving
            monthly_final_payment = calculateMonthlyFinalPayment(final_payment_amount, loan_term_years)
            combined_monthly_payment = monthly_loan_payment + monthly_final_payment
            monthly_saving, future_goal_target = calculate_monthly_saving(goal_target, current_savings, current_savings_return, savings_term_months, inflation_rate)   

            st.divider()
            
            # SAVE BUTTON
            if st.button('Calculate Car Plan'):
                # Save plan to DB
                plan_id = createPlan(user_id, goal_type, goal_name, selected_brand, selected_model, target_age, due_date, 
                            goal_total, goal_target, monthly_saving, 
                            current_savings, current_savings_return, savings_term_months,
                            loan_radio, down_payment_radio, final_payment_radio,
                            down_payment_percent, down_payment_amount, final_payment_percent, final_payment_amount, 
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
            due_date = calculateGoalDate(profile.user_birthday, target_age)
            goal_total = st.number_input(f'How much do you need at retirement (today\'s value, {currency_symbol})?', min_value=0.0, value=600000.0, key='pension_down_payment_amount')
            
            # Current saving
            col1_1, col1_2 = st.columns([1, 3])
            with col1_1:
                current_savings = st.number_input(f'Current retirement savings ({currency_symbol}, optional):', min_value=0.0, format="%.2f", key='current_savings')
            if current_savings > 0:
                with col1_2:
                    current_savings_return = st.slider('Annual return on current savings (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='current_savings_return', value=1.6)
            else:
                current_savings_return = 0

            savings_term_months = (target_age - current_age) * 12
            monthly_final_payment = 0.0
            combined_monthly_payment = 0.0
            goal_target = goal_total - current_savings
            monthly_saving, future_goal_target = calculate_monthly_saving(goal_target, current_savings, current_savings_return, savings_term_months, inflation_rate)
                
            st.divider()
            
            # SAVE BUTTON
            if st.button('Calculate Retirement Plan'):
                # Save plan to DB
                plan_id = createPlan(user_id, goal_type, goal_name, None, None, target_age, due_date, 
                            goal_total, goal_target, monthly_saving, 
                            current_savings, current_savings_return, savings_term_months,
                            None, None, None,
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
            goal_total = st.number_input(f"Enter the target amount ({currency_symbol}):", min_value=0.0, format="%.2f", value = 2000.00)
            target_age = st.number_input("Enter the age by which you want to achieve this goal:", min_value=current_age + 1, max_value=100, step=1, key='target_age', value=current_age + 1)
            due_date = calculateGoalDate(profile.user_birthday, target_age)
            
            # Current saving
            col1_1, col1_2 = st.columns([1, 3])
            with col1_1:
                current_savings = st.number_input(f'Current savings for this plan ({currency_symbol}, optional):', min_value=0.0, format="%.2f", key='current_savings')
            if current_savings > 0:
                with col1_2:
                    current_savings_return = st.slider('Annual return on current savings (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='current_savings_return', value=1.6)
            else:
                current_savings_return = 0

            st.divider()

            # LOAN OPTION
            col1_1, col1_2 = st.columns([2, 3])
            with col1_1:
                st.subheader('Choose an Option: 👉')
            with col1_2:
                loan_radio = st.radio("Do you want to take a loan to cover this goal?", ("Yes", "No"), index=1)
            
            if loan_radio == "Yes":
                st.divider()

                # Down payment
                col1_1, col1_2 = st.columns([1, 3])
                with col1_1:
                    down_payment_radio = st.radio("Is there a down payment?", ("Yes", "No"), index=1)
                if down_payment_radio == "Yes":
                    with col1_2:
                        down_payment_percent = st.slider('Down payment (%):', min_value=0.0, max_value=100.0, step=0.1, format="%.1f", key='down_payment_percent', value=20.00)
                        down_payment_amount = round(goal_total * (down_payment_percent / 100), 2)
                        st.write(f"👉 Down payment: {down_payment_amount:.2f} {profile.user_currency}")
                else:
                    down_payment_percent = 0.0
                    down_payment_amount = 0.0
                
                st.divider()

                # Final payment
                col1_1, col1_2 = st.columns([1, 3])
                with col1_1:
                    final_payment_radio = st.radio("Is there a final payment?", ("Yes", "No"), index=1)
                if final_payment_radio == "Yes":
                    with col1_2:
                        final_payment_percent = st.slider('Final payment (%):', min_value=0.0, max_value=100.0, step=0.1, format="%.1f", key='final_payment_percent', value=40.00)
                        final_payment_amount = round(goal_total * (final_payment_percent / 100), 2)  
                        st.write(f"👉 Final payment: {final_payment_amount:.2f} {profile.user_currency}")
                else:
                    final_payment_percent = 0.0
                    final_payment_amount = 0.0

                st.divider()

                loan_amount_input = goal_total - down_payment_amount - final_payment_amount if down_payment_amount > 0 else goal_total - current_savings
                # Loan option
                col1_1, col1_2 = st.columns([1, 3])
                with col1_1:
                    loan_amount = st.number_input(f'Loan amount ({currency_symbol}):', min_value=0.0, format="%.2f", value=loan_amount_input)
                with col1_2:
                    loan_interest_rate = st.slider('Loan interest rate (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='loan_interest_rate', value=5.7)
                loan_term_years = st.number_input('Loan term (years):', min_value=0, max_value=50, step=1, key='loan_term_years', value=20)
                loan_start_date = st.date_input("Loan start date:", min_value=current_date, key='loan_start_date', format="DD.MM.YYYY", value=due_date)  
                monthly_loan_payment = calculate_loan_payment(loan_amount, loan_interest_rate, loan_term_years)
                goal_target = down_payment_amount - current_savings if down_payment_amount > 0 else goal_total - loan_amount
                
            else:
                down_payment_percent = 0.0
                down_payment_amount = 0.0
                final_payment_percent = 0.0
                final_payment_amount = 0.0
                loan_amount = 0.0
                loan_interest_rate = 0.0
                loan_term_years = 0
                loan_start_date = current_date
                monthly_loan_payment = 0.0
                goal_target = goal_total - current_savings
                down_payment_radio = None
                final_payment_radio = None

            savings_term_months = (due_date.year - current_date.year) * 12 + (due_date.month - current_date.month)
            monthly_final_payment = calculateMonthlyFinalPayment(final_payment_amount, loan_term_years)
            combined_monthly_payment = monthly_loan_payment + monthly_final_payment
            monthly_saving, future_goal_target = calculate_monthly_saving(goal_target, current_savings, current_savings_return, savings_term_months, inflation_rate)   

            st.divider()
            
            # SAVE BUTTON
            if st.button('Calculate Custom Plan'):
                # Add plan to database
                plan_id = createPlan(user_id, goal_type, goal_name, None, None, target_age, due_date, 
                            goal_total, goal_target, monthly_saving, 
                            current_savings, current_savings_return, savings_term_months,
                            loan_radio, down_payment_radio, final_payment_radio,
                            down_payment_percent, down_payment_amount, final_payment_percent, final_payment_amount, 
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
