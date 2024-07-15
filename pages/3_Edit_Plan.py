import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import time
from db import getPlan, getUserInfo, calculateUserAge, logout, calculateGoalDate, updatePlan, createSaving, backToOverview, getSavings, getTotalSavings, deletePlan, showChosenPages
from financial_plan import generate_data_and_plot, calculateMonthlyFinalPayment, create_savings_graph, generate_monthly_data_and_plot
from financial_plan import calculate_monthly_saving, calculate_loan_payment, filter_models, calculate_pension_monthly_saving
import base64

showChosenPages()

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 加载 CSS 文件
css_file_path = "data/titlestyle.css"
load_css(css_file_path)

# Function to encode images in base64
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    return encoded_image

# Helper function to get a list of years
def get_years(start_year, end_year):
    return [str(year) for year in range(start_year, end_year + 1)]

def editing_page():
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        user_id = st.session_state.user_id

        if 'edit_plan_id' in st.session_state:

            @st.experimental_dialog("📊 Add Saving Progress")
            def add_saving(user_id, plan):
                profile = getUserInfo(user_id)
                st.header(f"Plan: {plan.goal_name}")

                months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                years = get_years(datetime.now().year - 3, datetime.now().year + 7)
                col1, col2 = st.columns([2, 1])
                selected_month = col1.selectbox ("📅 Select month", months, index=datetime.now().month - 1)
                selected_year = col2.selectbox("📅 Select year", years, index=years.index(str(datetime.now().year)))

                # Map the month name to its corresponding number
                month_number = months.index(selected_month) + 1

                # Combine selected_year, month_number, and day 01 into a date
                savings_date = datetime(int(selected_year), month_number, 1)

                #savings_date = st.date_input("📅 Select Date", value=datetime.today(), format="DD.MM.YYYY")
                savings_amount = st.number_input(f"🪙 Saving Amount for {savings_date.strftime('%B %Y')} ({profile.user_currency})", value=float(plan.goal_target_monthly))

                col1_1, col1_2 = st.columns([1, 1])
                with col1_1:
                    if st.button("✅ Submit"):
                        createSaving(user_id, plan.plan_id, savings_date, savings_amount)
                        st.success("Saving added successfully!")
                        time.sleep(0.3)
                        del st.session_state.add_saving_plan_id
                        st.rerun()
                        
                with col1_2:
                    if st.button("❌ Cancel"):
                        st.info("Saving canceled.")
                        time.sleep(0.3)
                        del st.session_state.add_saving_plan_id
                        st.rerun()

            # Get plan info
            plan_id = st.session_state.edit_plan_id
            plan = getPlan(plan_id)

            # Get user info
            user_id = st.session_state.user_id
            profile = getUserInfo(user_id)

            # Get saving info
            savings = getSavings(user_id, plan_id)
            total_saving = getTotalSavings(user_id, plan_id)

            # --- PERSONAL INFORMATION ---
            # PREPARATION

            # Calculate birthday
            current_age = calculateUserAge(profile.user_birthday)
            current_date = datetime.now().date()

            # PLAN OPTIONS
            page = plan.goal_type
            
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

            # Buttons
            backToOverview()
            logout()

            # --- House Buyer Savings Plan ---
            if page == "House Buyer Savings Plan":
                st.markdown(
                    f"""
                    <h1>🏡 {plan.goal_name}</h1>
                    """,
                    unsafe_allow_html=True
                )
                st.divider()
                goal_name = st.text_input("Name of the plan", value = plan.goal_name)
                house_price = st.number_input(f'House price ({currency_symbol}):', min_value=0.0, format="%.2f", key='house_price', value=float(plan.goal_total))
                target_age = st.number_input("Enter the age by which you want to achieve this goal:", min_value=current_age + 1, max_value=100, step=1, key='target_age', value=plan.goal_age)
                due_date = calculateGoalDate(profile.user_birthday, target_age)

                # Current saving
                col1_1, col1_2 = st.columns([1, 3])
                with col1_1:
                    current_savings = st.number_input(f'Current savings for the house ({currency_symbol}, optional):', min_value=0.0, format="%.2f", key='current_savings', value=float(plan.saving_initial))
                if current_savings > 0:
                    with col1_2:
                        current_savings_return = st.slider('Annual return on current savings (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='current_savings_return', value=float(plan.saving_interest))
                else:
                    current_savings_return = 0
        
                st.divider()

                # MORTGAGE LOAN
                col1_1, col1_2 = st.columns([2, 3])
                with col1_1:
                    st.subheader('Choose an Option: 👉')
                with col1_2:
                    take_house_loan = st.radio("Do you want to calculate the mortgage loan?", ("Yes", "No"), index= 0 if plan.loan_amount > 0 else 1)
                
                if take_house_loan == "Yes":
                    st.divider()
                    # Down payment
                    col1_1, col1_2 = st.columns([1, 3])
                    with col1_1:
                        down_payment_radio = st.radio("Is there a down payment?", ("Yes", "No"), index=0 if plan.payment_first_percent > 0 else 1)
                    if down_payment_radio == "Yes":
                        with col1_2:
                            down_payment_percent = st.slider('Down payment (%):', min_value=0.0, max_value=100.0, step=0.1, format="%.1f", key='down_payment_percent', value=float(plan.payment_first_percent))
                            down_payment_amount = round(house_price * (down_payment_percent / 100), 2)
                            st.write(f"👉 Down payment: {down_payment_amount:.2f} {profile.user_currency}")
                    else:
                        down_payment_percent = 0.0
                        down_payment_amount = 0.0
                    
                    st.divider()
                    
                    # Final payment
                    col1_1, col1_2 = st.columns([1, 3])
                    with col1_1:
                        final_payment_radio = st.radio("Is there a final payment?", ("Yes", "No"), index=0 if plan.payment_last_percent > 0 else 1)
                    if final_payment_radio == "Yes":
                        with col1_2:
                            final_payment_percent = st.slider('Final payment (%):', min_value=0.0, max_value=100.0, step=0.1, format="%.1f", key='final_payment_percent', value=float(plan.payment_last_percent))
                            final_payment_amount = round(house_price * (final_payment_percent / 100), 2)  
                            st.write(f"👉 Final payment: {final_payment_amount:.2f} {profile.user_currency}")
                    else:
                        final_payment_percent = 0.0
                        final_payment_amount = 0.0

                    st.divider()

                    loan_amount_input = house_price - down_payment_amount - final_payment_amount if down_payment_amount > 0 else house_price - current_savings
                
                    # Loan rate
                    col1_1, col1_2 = st.columns([1, 3])
                    with col1_1:
                        loan_amount = st.number_input(f'Mortgage loan amount ({currency_symbol}):', min_value=0.0, format="%.2f", value=loan_amount_input)
                    with col1_2:
                        loan_interest_rate = st.slider('Mortgage interest rate (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='loan_interest_rate', value=float(plan.loan_interest))
                    loan_term_years = st.number_input('Mortgage loan term (years):', min_value=0, max_value=50, step=1, key='loan_term_years', value=plan.loan_duration)
                    loan_start_date = st.date_input("Mortgage start date:", min_value=current_date, key='loan_start_date', format="DD.MM.YYYY", value="01.01.1900" if take_house_loan == "No" else plan.loan_startdate)  
                    monthly_loan_payment = calculate_loan_payment(loan_amount, loan_interest_rate, loan_term_years)
                    goal_target = down_payment_amount - current_savings if down_payment_amount > 0 else house_price - loan_amount
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
                    goal_target = house_price - current_savings

                # Calculate monthly saving
                savings_term_months = (due_date.year - current_date.year) * 12 + (due_date.month - current_date.month)
                monthly_saving, future_goal_target = calculate_monthly_saving(goal_target, current_savings, current_savings_return, savings_term_months, inflation_rate)   
                rest_saving = plan.goal_target - total_saving
                monthly_final_payment = calculateMonthlyFinalPayment(final_payment_amount, loan_term_years)
                combined_monthly_payment = monthly_loan_payment + monthly_final_payment

                st.divider()
            
                # SAVING PLAN OPTION 
                col1_1, col1_2 = st.columns([4, 1])
                with col1_1:
                    if st.button("💾 Save changes"):  
                        # Add plan to database
                        updatePlan(plan.plan_id, goal_name, target_age, due_date, 
                                    house_price, goal_target, monthly_saving, 
                                    current_savings, current_savings_return, savings_term_months,
                                    down_payment_percent, down_payment_amount, final_payment_percent, final_payment_amount, 
                                    loan_term_years, loan_start_date, loan_amount, loan_interest_rate, monthly_loan_payment)
                        # Write result
                        st.success("Plan updated successfully!") 
                with col1_2:
                    if st.button(f"🗑️ Delete", key=f"delete_{plan.plan_id}"):
                        deletePlan(plan.plan_id)
                        st.switch_page("Goaldigger.py")
                
                st.divider()
                
                st.subheader("Summary")

                if take_house_loan == "Yes":
                    tab1, tab2 = st.tabs(["📊 Financial Goal", "📝 Loan Details"])
                    with tab2:
                        st.write(f"**Loan Start Date**: {loan_start_date.strftime('%d.%m.%Y')}")
                        st.write(f"**Monthly Loan Payment**: <span style='color: blue;'>{monthly_loan_payment:,.2f} {currency_symbol}</span>", unsafe_allow_html=True)
                        if final_payment_percent > 0:
                            st.write(f"**Additional Savings Needed for Final Payment**: {monthly_final_payment:,.2f} {currency_symbol}")
                            st.write(f"**Combined Monthly Payment**: <span style='color: green;'>{combined_monthly_payment:,.2f} {currency_symbol}</span>", unsafe_allow_html=True)

                else:
                    tab1, = st.tabs(["📊 Financial Goal"])
            
                with tab1:
                    st.write(f"**Saving Target**: <span style='color: blue;'>{goal_target:,.2f} {currency_symbol}</span> by {due_date.strftime('%d.%m.%Y')} (including inflation: {future_goal_target:,.2f} {profile.user_currency})", unsafe_allow_html=True)
                    st.write(f"**Monthly Savings Required**: <span style='color: green;'>{monthly_saving:,.2f} {currency_symbol}</span> per month for <span style='color: green;'>{savings_term_months}</span> months", unsafe_allow_html=True)
                    st.write(f"**Current Savings**: <span style='color: red;'>{total_saving:,.2f} {currency_symbol}</span>", unsafe_allow_html=True)
                    st.write(f"**Amount Still Needed**: <span style='color: red;'>{rest_saving:,.2f} {currency_symbol}</span>", unsafe_allow_html=True)

                    if plan.goal_target > 0:
                        progress = min(float(total_saving / plan.goal_target), 1.0)
                        st.progress(progress)
                    else:
                        st.warning("Target amount for this plan is zero, cannot show graph.")
                
                st.markdown("</div>", unsafe_allow_html=True)

                # BUTTONS
                col1_1, col1_2 = st.columns([2, 1])
                with col1_1:
                    if st.button(f"📈 Grow your savings", key=f"invest_{plan.plan_id}"):
                        st.session_state.invest_plan_id = plan.plan_id
                        st.switch_page("pages/7_Risk_Tolerance_Assessment.py")
                with col1_2:
                    if st.button(f"✅ Add Saving", key=f"add_saving_{plan.plan_id}"):
                        st.session_state.add_saving_plan_id = plan.plan_id
                        add_saving(user_id, plan)

                st.divider()
                
                st.subheader("Statistics")
                tab1, tab2 = st.tabs(["📊 Plan Overview", "📝 Saving Progress"])
                with tab1:
                    if plan.goal_age - current_age > 1:
                        # Call the function to generate data and plot
                        generate_data_and_plot(plan_id, current_savings, savings_term_months, goal_target, loan_term_years, monthly_saving, monthly_loan_payment, monthly_final_payment, currency_symbol)
                    else:
                        # Call the function to generate data and plot
                        generate_monthly_data_and_plot(plan_id, current_savings, savings_term_months, goal_target, loan_term_years, monthly_saving, monthly_loan_payment, monthly_final_payment, currency_symbol)

                with tab2:
                    if plan.goal_target > 0:
                        create_savings_graph(plan_id)
                    else:
                        st.warning("Target amount for this plan is zero, cannot show graph.")

                st.divider()
            
                # Mortgage ads
                st.markdown(
                    f"""
                    <h2 class="custom-subheader">Your Local Mortgage Providers</h2>
                    """,
                    unsafe_allow_html=True
                )
                ads = [
                    {
                        "company":" ",
                        "description": "We have been assisting Expats for more than 20 years to secure their German mortgage. An easy English speaking step-by-step service which is free of charge. Blue-Card holders welcome. Five star Google Reviews from our clients prove our services.",
                        "link_text": "View more",
                        "link": "https://your-german-mortgage.de/",
                        "image_path": "img/image_removebg_preview.png",
                        "button_background_color": "#9e8360",
                        "button_text_color": "#ffffff"

                    },
                    {
                        "company":" ",
                        "description": "Baufi24 is Germany’s first digital mortgage broker. Baufi24 combines smart technology and certified mortgage advice to help clients save time and money while making property purchasing in Germany transparent and hassle-free.",
                        "link_text": "View more",
                        "link": "https://www.baufi24.de",
                        "image_path": "img/baufi.png",
                        "button_background_color": "#d5fdcf",
                        "button_text_color": "#0e2a47"
                    },
                    {
                        "company":" ",
                        "description": "finbird digital provides English mortgage and property consulting for international professionals throughout Germany. We help with checking your property budget and affordability at an early stage and with guiding you along the purchase process until transaction close. We educate about the buying process and mortgage financing options with recurring events and comprehensive educational guides.",
                        "link_text": "View more",
                        "link": "https://www.finbird.digital",
                        "image_path": "img/finbird.png",
                        "button_background_color": "#5cb6d5",
                        "button_text_color": "#ffffff"
                    },
                    {
                        "company":" ",
                        "description": "Hypofriend is Germany’s smartest mortgage broker, built by PhDs and engineers they calculate the optimal mortgage for your situation. Their English-speaking mortgage experts will guide you through the entire process giving you insights along the way, free of charge.",
                        "link_text": "View more",
                        "link": "https://www.hypofriend.de",
                        "image_path": "img/hypofriend.png",
                        "button_background_color": "#3f818f",
                        "button_text_color": "#ffffff"
                    } 
                ]
                colors = ["#ffffff", "#0c2c4c", "#24243c", "#ffffff", "#fff3e0"] 
                text_colors = ["#333333", "#ffffff", "#ffffff", "##547e8c", "#333333"]
                button_text_color = ["#24243c", "#ffffff", "#24243c", "#ffffff", "#24243c"] 
                
                col1, col2 = st.columns(2)
                for i, ad in enumerate(ads):
                    encoded_image = get_base64_image(ad["image_path"])
                    background_color = colors[i % len(colors)]
                    button_text_color = colors[i % len(button_text_color)]
                    text_color = text_colors[i % len(text_colors)]
                    button_background_color = ad.get("button_background_color", "#000000")  # Default to black if not provided
                    button_text_color = ad.get("button_text_color", "#ffffff")    
                    with col1 if i % 2 == 0 else col2:
                        st.markdown(f"""
                         <div style="background-color:{background_color}; padding: 10px; margin: 10px; border-radius: 10px; color: {text_color};">
                            <h3 style="color: {text_color};">{ad['company']}</h3>
                            <img src="data:image/png;base64,{encoded_image}" width="100%" style="margin: 10px 0;">
                            <p style="color: {text_color};">{ad['description']}</p>
                            <a href="{ad['link']}" target="_blank" style="text-decoration: none;">
                                <button style="background-color: {button_background_color}; color: {button_text_color}; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 10px 2px; cursor: pointer; border-radius: 5px;">{ad['link_text']}</button>
                            </a>
                        </div>
                        """, unsafe_allow_html=True)

            # --- CAR BUYER SAVINGS PLAN ----
            if page == "Car Buyer Savings Plan":
                st.markdown(
                    f"""
                    <h1>🚘 {plan.goal_name}</h1>
                    """,
                    unsafe_allow_html=True
                )
                # Enter goal name
                goal_name = st.text_input("Name of the plan", value = plan.goal_name)

                df = pd.read_excel("data/car_prices.xlsx")

                st.markdown(
                    f"""
                    <h2 class="custom-subheader">Choose an Option:</h2>
                    """,
                    unsafe_allow_html=True
                )
                savings_option = st.radio('', ('See Available Suggested Car Prices', 'Input Your Car Price'))

                if savings_option == 'See Available Suggested Car Prices':
                    st.markdown(
                    f"""
                    <h2 class="custom-subheader">See Available Suggested Car Prices</h2>
                    """,
                    unsafe_allow_html=True
                )

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
                    st.markdown(
                    f"""
                    <h2 class="custom-subheader">Input Your Car Price</h2>
                    """,
                    unsafe_allow_html=True
                    )
                    car_price_input = st.number_input('Enter the total cost of the car:', min_value=0.0, format="%.2f", key='adjusted_car_price')
                
                # Calculate age and date
                target_age = st.number_input('Enter the age you wish to buy the car:', min_value=current_age + 1, max_value=100, step=1, key='car_target_age', value=plan.goal_age)
                due_date = calculateGoalDate(profile.user_birthday, target_age)
                savings_term_months = (target_age - current_age) * 12
                
                # Current saving
                col1_1, col1_2 = st.columns([1, 3])
                with col1_1:
                    current_savings = st.number_input(f'Current savings for the car ({currency_symbol}, optional):', min_value=0.0, format="%.2f", key='current_savings', value=float(plan.saving_initial))
                if current_savings > 0:
                    with col1_2:
                        current_savings_return = st.slider('Annual return on current savings (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='current_savings_return', value=float(plan.saving_interest))
                else:
                    current_savings_return = 0
                
                st.divider()

                # CAR LOAN
                col1_1, col1_2 = st.columns([2, 3])
                with col1_1:
                    st.subheader('Choose an Option: 👉')
                with col1_2:
                    take_car_loan = st.radio("Do you want to calculate the car loan?", ("Yes", "No"), index=0 if plan.loan_amount > 0 else 1)
                
                if take_car_loan == "Yes":
                    st.divider()

                    # Down payment
                    col1_1, col1_2 = st.columns([1, 3])
                    with col1_1:
                        down_payment_radio = st.radio("Is there a down payment?", ("Yes", "No"), index=0 if plan.payment_first_percent > 0 else 1)
                    if down_payment_radio == "Yes":
                        with col1_2:
                            down_payment_percent = st.slider('Down payment (%):', min_value=0.0, max_value=100.0, step=0.1, format="%.1f", key='down_payment_percent', value=float(plan.payment_first_percent))
                            down_payment_amount = round(car_price_input * (down_payment_percent / 100), 2)
                            st.write(f"👉 Down payment: {down_payment_amount:.2f} {profile.user_currency}")
                    else:
                        down_payment_percent = 0.0
                        down_payment_amount = 0.0
                    
                    st.divider()

                    # Final payment
                    col1_1, col1_2 = st.columns([1, 3])
                    with col1_1:
                        final_payment_radio = st.radio("Is there a final payment?", ("Yes", "No"), index=0 if plan.payment_last_percent > 0 else 1)
                    if final_payment_radio == "Yes":
                        with col1_2:
                            final_payment_percent = st.slider('Final payment (%):', min_value=0.0, max_value=100.0, step=0.1, format="%.1f", key='final_payment_percent', value=float(plan.payment_last_percent))
                            final_payment_amount = round(car_price_input * (final_payment_percent / 100), 2)  
                            st.write(f"👉 Final payment: {final_payment_amount:.2f} {profile.user_currency}")
                    else:
                        final_payment_percent = 0.0
                        final_payment_amount = 0.0

                    st.divider()

                    loan_amount_input = car_price_input - down_payment_amount - final_payment_amount if down_payment_amount > 0 else car_price_input - current_savings
                
                    # Loan rate
                    col1_1, col1_2 = st.columns([1, 3])
                    with col1_1:
                        loan_amount = st.number_input(f'Car loan amount ({currency_symbol}):', min_value=0.0, format="%.2f", value=loan_amount_input)
                    with col1_2:
                        loan_interest_rate = st.slider('Car loan interest rate (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='loan_interest_rate', value=float(plan.loan_interest))
                    loan_term_years = st.number_input('Car loan term (years):', min_value=0, max_value=50, step=1, key='loan_term_years', value=plan.loan_duration)
                    loan_start_date = st.date_input("Car loan start date:", min_value=current_date, key='loan_start_date', format="DD.MM.YYYY", value=current_date if take_car_loan == "No" else plan.loan_startdate)  
                    monthly_loan_payment = calculate_loan_payment(loan_amount, loan_interest_rate, loan_term_years)
                    goal_target = down_payment_amount - current_savings if down_payment_amount > 0 else car_price_input - loan_amount
                
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
                    goal_target = car_price_input - current_savings

                # Calculate monthly saving
                monthly_saving, future_goal_target = calculate_monthly_saving(goal_target, current_savings, current_savings_return, savings_term_months, inflation_rate)
                rest_saving = plan.goal_target - total_saving
                monthly_final_payment = calculateMonthlyFinalPayment(final_payment_amount, loan_term_years)
                combined_monthly_payment = monthly_loan_payment + monthly_final_payment

                st.divider()
            
                col1_1, col1_2 = st.columns([4, 1])
                with col1_1:
                    if st.button("💾 Save changes"):
                        # Save plan to DB
                        updatePlan(plan.plan_id, goal_name, target_age, due_date, 
                                    car_price_input, goal_target, monthly_saving, 
                                    current_savings, current_savings_return, savings_term_months,
                                    down_payment_percent, down_payment_amount, final_payment_percent, final_payment_amount, 
                                    loan_term_years, loan_start_date, loan_amount, loan_interest_rate, monthly_loan_payment)
                        
                        # Write result
                        st.success("Plan updated successfully!")
                with col1_2:
                    if st.button(f"🗑️ Delete", key=f"delete_{plan.plan_id}"):
                        deletePlan(plan.plan_id)
                        st.switch_page("Goaldigger.py")
                   
                st.divider()
                
                st.subheader("Summary")
                if take_car_loan == "Yes":
                    tab1, tab2 = st.tabs(["📊 Financial Goal", "📝 Loan Details"])
                    with tab2:
                        st.write(f"**Loan Start Date**: {loan_start_date.strftime('%d.%m.%Y')}")
                        st.write(f"**Monthly Loan Payment**: <span style='color: blue;'>{monthly_loan_payment:,.2f} {currency_symbol}</span>", unsafe_allow_html=True)
                        if final_payment_percent > 0:
                            st.write(f"**Additional Savings Needed for Final Payment**: {monthly_final_payment:,.2f} {currency_symbol}")
                            st.write(f"**Combined Monthly Payment**: <span style='color: green;'>{combined_monthly_payment:,.2f} {currency_symbol}</span>", unsafe_allow_html=True)

                else:
                    tab1, = st.tabs(["📊 Financial Goal"])

                with tab1:
                    st.write(f"**Saving Target**: <span style='color: blue;'>{goal_target:,.2f} {currency_symbol}</span> by {due_date.strftime('%d.%m.%Y')} (including inflation: {future_goal_target:,.2f} {profile.user_currency})", unsafe_allow_html=True)
                    st.write(f"**Monthly Savings Required**: <span style='color: green;'>{monthly_saving:,.2f} {currency_symbol}</span> per month for <span style='color: green;'>{savings_term_months}</span> months", unsafe_allow_html=True)
                    st.write(f"**Current Savings**: <span style='color: red;'>{total_saving:,.2f} {currency_symbol}</span>", unsafe_allow_html=True)
                    st.write(f"**Amount Still Needed**: <span style='color: red;'>{rest_saving:,.2f} {currency_symbol}</span>", unsafe_allow_html=True)
                    if plan.goal_target > 0:
                        progress = min(float(total_saving / plan.goal_target), 1.0)
                        st.progress(progress)
                    else:
                        st.warning("Target amount for this plan is zero, cannot show graph.")
                
                st.markdown("</div>", unsafe_allow_html=True)

                # BUTTONS
                col1_1, col1_2 = st.columns([2, 1])
                with col1_1:
                    if st.button(f"📈 Grow your savings", key=f"invest_{plan.plan_id}"):
                        st.session_state.invest_plan_id = plan.plan_id
                        st.switch_page("pages/7_Risk_Tolerance_Assessment.py")
                with col1_2:
                    if st.button(f"✅ Add Saving", key=f"add_saving_{plan.plan_id}"):
                        st.session_state.add_saving_plan_id = plan.plan_id
                        add_saving(user_id, plan)

                st.divider()
                
                st.subheader("Statistics")
                tab1, tab2 = st.tabs(["📊 Plan Overview", "📝 Saving Progress"])
                with tab1:
                    if plan.goal_age - current_age > 1:
                        # Call the function to generate data and plot
                        generate_data_and_plot(plan_id, current_savings, savings_term_months, goal_target, loan_term_years, monthly_saving, monthly_loan_payment, monthly_final_payment, currency_symbol)
                    else:
                        # Call the function to generate data and plot
                        generate_monthly_data_and_plot(plan_id, current_savings, savings_term_months, goal_target, loan_term_years, monthly_saving, monthly_loan_payment, monthly_final_payment, currency_symbol)

                with tab2:
                    if plan.goal_target > 0:
                        create_savings_graph(plan_id)
                    else:
                        st.warning("Target amount for this plan is zero, cannot show graph.")


            # --- RETIREMENT SAVINGS PLAN ----
            if page == "Retirement Savings Plan":
                st.markdown(
                    f"""
                    <h1>👵🏼 {plan.goal_name}</h1>
                    """,
                    unsafe_allow_html=True
                )

                # Enter goal name
                goal_name = st.text_input("Name of the plan", value = plan.goal_name)
                target_age = st.number_input('When do you want to retire?', min_value=current_age + 1, max_value=100, key='target_age', value=plan.goal_age)
                due_date = calculateGoalDate(profile.user_birthday, target_age)
                retirement_amount = st.number_input(f'How much do you need at retirement (today\'s value, {currency_symbol})?', min_value=0.0, value=float(plan.goal_total))
                
                # Current saving
                col1_1, col1_2 = st.columns([1, 3])
                with col1_1:
                    current_savings = st.number_input(f'Current retirement savings ({currency_symbol}, optional):', min_value=0.0, format="%.2f", key='current_savings', value = float(plan.saving_initial))
                if current_savings > 0:
                    with col1_2:
                        current_savings_return = st.slider('Annual return on current savings (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='current_savings_return', value=float(plan.saving_interest))
                else:
                    current_savings_return = 0             
                
                savings_term_months = (target_age - current_age) * 12
                savings_term_years = target_age - current_age

                monthly_saving = calculate_pension_monthly_saving(retirement_amount, current_savings, current_savings_return, savings_term_months)
                rest_saving = plan.goal_target - total_saving
                monthly_final_payment = 0
                combined_monthly_payment = 0

                st.divider()
            
                # SAVING PLAN OPTION 
                col1_1, col1_2 = st.columns([4, 1])
                with col1_1:
                    if st.button("💾 Save changes"):  
                        # Save plan to DB
                        updatePlan(plan.plan_id, goal_name, target_age, due_date, 
                                    retirement_amount, retirement_amount, monthly_saving, 
                                    current_savings, current_savings_return, savings_term_months,
                                    0, savings_term_months, 0, 0, 
                                    0, '1900-01-01', 0, 0, 0)
                        
                        # Write result
                        st.success("Plan updated successfully!")
                with col1_2:
                    if st.button(f"🗑️ Delete", key=f"delete_{plan.plan_id}"):
                        deletePlan(plan.plan_id)
                        st.switch_page("Goaldigger.py")

                st.divider()

                st.subheader("Summary")

                tab1, = st.tabs(["📊 Financial Goal"])
                with tab1:
                    st.write(f"**Saving Target**: <span style='color: blue;'>{retirement_amount:,.2f} {currency_symbol}</span> by {due_date.strftime('%d.%m.%Y')}", unsafe_allow_html=True)
                    st.write(f"**Monthly Savings Required**: <span style='color: green;'>{monthly_saving:,.2f} {currency_symbol}</span> per month for <span style='color: green;'>{savings_term_months}</span> months", unsafe_allow_html=True)
                    st.write(f"**Current Savings**: <span style='color: red;'>{total_saving:,.2f} {currency_symbol}</span>", unsafe_allow_html=True)
                    st.write(f"**Amount Still Needed**: <span style='color: red;'>{rest_saving:,.2f} {currency_symbol}</span>", unsafe_allow_html=True)

                    if plan.goal_target > 0:
                        progress = min(float(total_saving / plan.goal_target), 1.0)
                        st.progress(progress)
                    else:
                        st.warning("Target amount for this plan is zero, cannot show graph.")
                
                st.markdown("</div>", unsafe_allow_html=True)

                # BUTTONS
                col1_1, col1_2 = st.columns([2, 1])
                with col1_1:
                    if st.button(f"📈 Grow your savings", key=f"invest_{plan.plan_id}"):
                        st.session_state.invest_plan_id = plan.plan_id
                        st.switch_page("pages/7_Risk_Tolerance_Assessment.py")
                with col1_2:
                    if st.button(f"✅ Add Saving", key=f"add_saving_{plan.plan_id}"):
                        st.session_state.add_saving_plan_id = plan.plan_id
                        add_saving(user_id, plan)

                st.divider()
                
                st.subheader("Statistics")
                tab1, tab2 = st.tabs(["📊 Plan Overview", "📝 Saving Progress"])
                with tab1:
                    if plan.goal_age - current_age > 1:               
                        # Call the function to generate data and plot
                        generate_data_and_plot(plan_id, current_savings, savings_term_months, retirement_amount, 0, monthly_saving, 0, 0, currency_symbol)
                    else:
                        # Call the function to generate data and plot
                        generate_monthly_data_and_plot(plan_id, current_savings, savings_term_months, goal_target, loan_term_years, monthly_saving, monthly_loan_payment, monthly_final_payment, currency_symbol)

                with tab2:
                    if plan.goal_target > 0:
                        create_savings_graph(plan_id)
                    else:
                        st.warning("Target amount for this plan is zero, cannot show graph.")

            # --- CUSTOMIZED FINANCIAL PLAN ---
            if page == "Customized Financial Plan":
                st.markdown(
                    f"""
                    <h1>🔧 {plan.goal_name}</h1>
                    """,
                    unsafe_allow_html=True
                )

                # Inputs for custom financial plan
                goal_name = st.text_input("Enter the name of your plan:", value = plan.goal_name)
                goal_total = st.number_input(f"Enter the target amount ({currency_symbol}):", min_value=0.0, format="%.2f", value=float(plan.goal_total))
                target_age = st.number_input("Enter the age by which you want to achieve this goal:", min_value=current_age + 1, max_value=100, step=1, key='target_age', value=plan.goal_age)
                due_date = calculateGoalDate(profile.user_birthday, target_age)
                
                # Current saving
                col1_1, col1_2 = st.columns([1, 3])
                with col1_1:
                    current_savings = st.number_input(f'Current savings for this plan ({currency_symbol}, optional):', min_value=0.0, format="%.2f", key='current_savings', value=float(plan.saving_initial))
                if current_savings > 0:
                    with col1_2:
                        current_savings_return = st.slider('Annual return on current savings (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='current_savings_return', value=float(plan.saving_interest))
                else:
                    current_savings_return = 0

                st.divider()
  
                rest_saving = plan.goal_target - total_saving

                # LOAN OPTION
                col1_1, col1_2 = st.columns([2, 3])
                with col1_1:
                    st.subheader('Choose an Option: 👉')
                with col1_2:
                    loan_option = st.radio("Do you want to take a loan to cover this goal?", ("Yes", "No"), index=0 if plan.loan_amount > 0 else 1)
                
                if loan_option == "Yes":
                    st.divider()

                    # Down payment
                    col1_1, col1_2 = st.columns([1, 3])
                    with col1_1:
                        down_payment_radio = st.radio("Is there a down payment?", ("Yes", "No"), index=0 if plan.payment_first_percent > 0 else 1)
                    if down_payment_radio == "Yes":
                        with col1_2:
                            down_payment_percent = st.slider('Down payment (%):', min_value=0.0, max_value=100.0, step=0.1, format="%.1f", key='down_payment_percent', value=float(plan.payment_first_percent))
                            down_payment_amount = round(goal_total * (down_payment_percent / 100), 2)
                            st.write(f"👉 Down payment: {down_payment_amount:.2f} {profile.user_currency}")
                    else:
                        down_payment_percent = 0.0
                        down_payment_amount = 0.0
                    
                    st.divider()

                    # Final payment
                    col1_1, col1_2 = st.columns([1, 3])
                    with col1_1:
                        final_payment_radio = st.radio("Is there a final payment?", ("Yes", "No"), index=0 if plan.payment_last_percent > 0 else 1)
                    if final_payment_radio == "Yes":
                        with col1_2:
                            final_payment_percent = st.slider('Final payment (%):', min_value=0.0, max_value=100.0, step=0.1, format="%.1f", key='final_payment_percent', value=float(plan.payment_last_percent))
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
                        loan_term_years = st.number_input('Loan term (years):', min_value=0, max_value=30, step=1, value=plan.loan_duration)
                    loan_interest_rate = st.slider('Loan interest rate (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", value = float(plan.loan_interest))
                    loan_start_date = st.date_input("Loan start date:", value=plan.loan_startdate, format="DD.MM.YYYY")
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
                    
                savings_term_months = (due_date.year - current_date.year) * 12 + (due_date.month - current_date.month)
                monthly_final_payment = calculateMonthlyFinalPayment(final_payment_amount, loan_term_years)
                combined_monthly_payment = monthly_loan_payment + monthly_final_payment
                monthly_saving, future_goal_target = calculate_monthly_saving(goal_target, current_savings, current_savings_return, savings_term_months, inflation_rate)

                st.divider()
            
                # SAVING PLAN OPTION 
                col1_1, col1_2 = st.columns([4, 1])
                with col1_1:
                    if st.button("💾 Save changes"):  
                        # Save plan to DB
                        updatePlan(plan.plan_id, goal_name, target_age, due_date, 
                                    goal_total, goal_target, monthly_saving, 
                                    current_savings, current_savings_return, savings_term_months,
                                    down_payment_percent, down_payment_amount, final_payment_percent, final_payment_amount, 
                                    loan_term_years, loan_start_date, loan_amount, loan_interest_rate, monthly_loan_payment)
                        
                        # Write result
                        st.success("Plan updated successfully!")
                with col1_2:
                    if st.button(f"🗑️ Delete", key=f"delete_{plan.plan_id}"):
                        deletePlan(plan.plan_id)
                        st.switch_page("Goaldigger.py")

                st.divider()
            
                st.subheader("Summary")

                if loan_option == "Yes":
                    tab1, tab2 = st.tabs(["📊 Financial Goal", "📝 Loan Details"])
                    with tab2:
                        st.write(f"### Loan Details")
                        st.write(f"**Loan Start Date**: {loan_start_date.strftime('%d.%m.%Y')}")
                        st.write(f"**Monthly Loan Payment**: <span style='color: blue;'>{monthly_loan_payment:,.2f} {currency_symbol}</span>", unsafe_allow_html=True)
                        if final_payment_percent > 0:
                            st.write(f"**Additional Savings Needed for Final Payment**: {monthly_final_payment:,.2f} {currency_symbol}")
                            st.write(f"**Combined Monthly Payment**: <span style='color: green;'>{combined_monthly_payment:,.2f} {currency_symbol}</span>", unsafe_allow_html=True)
                
                else:
                    tab1, = st.tabs(["📊 Financial Goal"])

                with tab1:
                    st.write(f"**Saving Target**: <span style='color: blue;'>{goal_target:,.2f} {currency_symbol}</span> by {due_date.strftime('%d.%m.%Y')} (including inflation: {future_goal_target:,.2f} {profile.user_currency})", unsafe_allow_html=True)
                    st.write(f"**Monthly Savings Required**: <span style='color: green;'>{monthly_saving:,.2f} {currency_symbol}</span> per month for <span style='color: green;'>{savings_term_months}</span> months", unsafe_allow_html=True)
                    st.write(f"**Current Savings**: <span style='color: red;'>{total_saving:,.2f} {currency_symbol}</span>", unsafe_allow_html=True)
                    st.write(f"**Amount Still Needed**: <span style='color: red;'>{rest_saving:,.2f} {currency_symbol}</span>", unsafe_allow_html=True)

                    if plan.goal_target > 0:
                        progress = min(float(total_saving / plan.goal_target), 1.0)
                        st.progress(progress)
                    else:
                        st.warning("Target amount for this plan is zero, cannot show graph.")
                
                st.markdown("</div>", unsafe_allow_html=True)

                # BUTTONS
                col1_1, col1_2 = st.columns([2, 1])
                with col1_1:
                    if st.button(f"📈 Grow your savings", key=f"invest_{plan.plan_id}"):
                        st.session_state.invest_plan_id = plan.plan_id
                        st.switch_page("pages/7_Risk_Tolerance_Assessment.py")
                with col1_2:
                    if st.button(f"✅ Add Saving", key=f"add_saving_{plan.plan_id}"):
                        st.session_state.add_saving_plan_id = plan.plan_id
                        add_saving(user_id, plan)

                st.divider()
                
                st.subheader("Statistics")
                tab1, tab2 = st.tabs(["📊 Plan Overview", "📝 Saving Progress"])
                with tab1:
                    if plan.goal_age - current_age > 1:
                        # Call the function to generate data and plot
                        generate_data_and_plot(plan_id, current_savings, savings_term_months, goal_target, loan_term_years, monthly_saving, monthly_loan_payment, monthly_final_payment, currency_symbol)
                    else:
                        # Call the function to generate data and plot
                        generate_monthly_data_and_plot(plan_id, current_savings, savings_term_months, goal_target, loan_term_years, monthly_saving, monthly_loan_payment, monthly_final_payment, currency_symbol)

                with tab2:
                    if plan.goal_target > 0:
                        create_savings_graph(plan_id)
                    else:
                        st.warning("Target amount for this plan is zero, cannot show graph.")
        
        else: 
            st.error("No plan selected for editing.")
            return

    else:
        st.warning("Please log in to access this page.")
        st.stop()

if __name__ == "__main__":
    editing_page()
