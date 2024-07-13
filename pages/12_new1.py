import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, date
from datetime import datetime, timedelta

# Custom color palette extracted from the provided image: todo
custom_colors = ['#7FDBFF', '#2ECC40', '#39CCCC', '#3D9970', '#FFDC00']

# Initialize session state for plans if not already set
if 'plans' not in st.session_state:
    st.session_state['plans'] = []


# Personal Information
st.sidebar.header('Personal Info')
user_name = st.sidebar.text_input('What is your name?')
birthdate = st.sidebar.date_input('When is your birthday?', min_value=date(1900, 1, 1), max_value=date.today() - timedelta(days=18 * 365))
current_age = calculate_age(birthdate)

# Country selection
country_data = {
    'Germany': {'Currency': 'EUR', 'Inflation rate': 5.9, 'LifeExpectancy': 80.7},
    'United Kingdom': {'Currency': 'GBP', 'Inflation rate': 6.8, 'LifeExpectancy': 82.1},
    'United States': {'Currency': 'USD', 'Inflation rate': 4.1, 'LifeExpectancy': 77.4}
}

selected_country = st.sidebar.selectbox('Select your country:', list(country_data.keys()))
currency = country_data[selected_country]['Currency']
inflation_rate = st.sidebar.slider('Annual inflation rate (%)', min_value=0.0, max_value=10.0, value=country_data[selected_country]['Inflation rate'], step=0.1, key='annual_inflation_rate')

# Currency symbols dictionary
currency_symbols = {
    'USD': '$',
    'EUR': '€',
    'GBP': '£'
}
currency_symbol = currency_symbols[currency]

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "House Buyer Savings Plan", "Car Buyer Savings Plan", "Retirement Savings Plan", "Customized Financial Plan"])





# CSS for custom styling
st.markdown("""
    <style>
    .plan-box {
        background-color: #f4f4f4;
        padding: 10px;
        margin: 10px;
        border-radius: 10px;
        width: 100%;
    }
    .loan-box {
        background-color: #e0f7fa;
        padding: 10px;
        margin: 10px;
        border-radius: 10px;
    }
    .delete-button {
        background-color: red;
        color: white;
        border: none;
        padding: 5px 10px;
        cursor: pointer;
    }
    .savings-term {
        margin-top: 5px;
    }
    #wholetext {
        border: 2px solid #ddd;
        padding: 10px;
        background-color: #f4f4f4;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# House Buyer Savings Plan
if page == "House Buyer Savings Plan":
    st.title("House Buyer Savings Plan")

    house_price = st.number_input(f'House price ({currency_symbol}):', min_value=0.0, format="%.2f", key='house_price')
    house_down_payment_percent = st.slider('Down payment percentage:', min_value=0.0, max_value=100.0, step=0.1, format="%.1f", key='house_down_payment_percent')

    house_target_age = st.number_input("Enter the age by which you want to achieve this goal:", min_value=current_age + 1, max_value=100, step=1, key='house_target_age')
    house_current_savings = st.number_input(f'Current savings for the house ({currency_symbol}, optional):', min_value=0.0, format="%.2f", key='house_current_savings')

    house_current_savings_return = 0
    if house_current_savings > 0:
        house_current_savings_return = st.slider('Annual return on current savings (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='house_current_savings_return')

    take_house_loan = st.radio("Do you want to take a mortgage loan?", ("Yes", "No"))

    if take_house_loan == "Yes":
        house_price_float = float(house_price)  # Ensure house_price is a float
        down_payment_amount = house_price_float * (house_down_payment_percent / 100)
        mortgage_loan_amount = house_price_float - down_payment_amount

        mortgage_interest_rate = st.slider('Mortgage interest rate (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='mortgage_interest_rate')
        mortgage_loan_term = st.number_input('Mortgage loan term (years):', min_value=1, max_value=30, step=1, key='mortgage_loan_term')
        mortgage_start_date = st.date_input("Mortgage start date:", min_value=date.today(), key='mortgage_start_date')

    if st.button('Calculate House Buyer Saving Plan'):
        house_target_date = datetime.now().replace(year=datetime.now().year + (house_target_age - current_age))
        current_date = datetime.now().date()
        if house_target_date.date() <= current_date:
            st.error("Target date must be in the future.")
        else:
            savings_term_months = (house_target_date.year - current_date.year) * 12 + (house_target_date.month - current_date.month)
            monthly_saving = calculate_monthly_saving(house_price * (house_down_payment_percent / 100), house_current_savings, house_current_savings_return, savings_term_months, inflation_rate)

            plan = {
                "name": "Buy a House",
                "target_amount": house_price * (house_down_payment_percent / 100),
                "due_date": house_target_date,
                "monthly_saving": monthly_saving,
                "savings_term_months": savings_term_months,
                "details_link": "House Buyer Savings Plan"
            }
            if take_house_loan == "Yes":
                plan['loan_amount'] = mortgage_loan_amount
                plan['loan_term'] = mortgage_loan_term
                plan['loan_interest_rate'] = mortgage_interest_rate
                plan['loan_start_date'] = mortgage_start_date
                monthly_loan_payment, total_loan_payment = calculate_loan(mortgage_loan_amount, mortgage_interest_rate, mortgage_loan_term)
                plan['monthly_loan_payment'] = monthly_loan_payment
                plan['total_loan_payment'] = total_loan_payment
                plan['custom_loan_end_date'] = mortgage_start_date + pd.DateOffset(years=mortgage_loan_term)

        

            if take_house_loan == "Yes":
                st.write(f"**Monthly Mortgage Payment:** <span style='color: blue;'>{currency_symbol}{monthly_loan_payment:,.2f}</span>", unsafe_allow_html=True)
                st.write(f"**Total Mortgage Payment:** {currency_symbol}{total_loan_payment:,.2f}")

                
# Car Buyer Savings Plan
if page == "Car Buyer Savings Plan":
    st.title("Car Buyer Savings Plan")

    file_path = "C:/Users/thaon/OneDrive/Documents/BFA/FIWP/car_prices.xlsx"
    df = load_car_data(file_path)

    st.header('Choose an Option:')
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

        adjusted_car_price = st.number_input('Adjust the car price if needed:', min_value=0.0, format="%.2f", value=float(price) if selected_model else 0.0, key='adjusted_car_price')
    else:
        st.subheader('Input Your Car Price')
        adjusted_car_price = st.number_input('Enter the total cost of the car:', min_value=0.0, format="%.2f", key='adjusted_car_price')

    down_payment_percent = st.slider('Enter your down payment percentage:', min_value=0.0, max_value=100.0, step=1.0, key='car_down_payment_percent')
    target_age = st.number_input('Enter the age you wish to buy the car:', value=30, min_value=0, max_value=100, step=1, key='car_target_age')
    car_current_savings = st.number_input(f'Current savings for the car ({currency_symbol}, optional):', min_value=0.0, format="%.2f", key='car_current_savings')

    car_current_savings_return = 0
    if car_current_savings > 0:
        car_current_savings_return = st.slider('Annual return on current savings (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='car_current_savings_return')

    take_car_loan = st.radio("Do you want to take a car loan?", ("Yes", "No"))

    if take_car_loan == "Yes":
        car_price_float = float(adjusted_car_price)  # Ensure adjusted_car_price is a float
        down_payment_amount = car_price_float * (float(down_payment_percent) / 100)
        car_loan_amount = st.number_input(f'Car loan amount ({currency_symbol}):', min_value=0.0, format="%.2f", value=0.0 if adjusted_car_price == 0 else car_price_float - down_payment_amount)
        car_loan_interest_rate = st.slider('Car loan interest rate (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='car_loan_interest_rate')
        car_loan_term = st.number_input('Car loan term (years):', min_value=0, max_value=30, step=1, key='car_loan_term_years')
        car_loan_start_date = st.date_input("Car loan start date:", min_value=date.today(), key='car_loan_start_date')

    if st.button('Calculate Car Buyer Savings Plan'):
        if target_age <= current_age:
            st.error("The target age must be greater than the current age.")
        else:
            monthly_savings_needed = calculate_car_savings(adjusted_car_price, down_payment_percent, current_age, target_age, car_current_savings, car_current_savings_return, inflation_rate)
            plan = {
                "name": "Buy a Car",
                "target_amount": adjusted_car_price * (down_payment_percent / 100),
                "due_date": datetime.now().replace(year=datetime.now().year + (target_age - current_age)),
                "monthly_saving": monthly_savings_needed,
                "savings_term_months": (target_age - current_age) * 12,
                "details_link": "Car Buyer Savings Plan"
            }

            if take_car_loan == "Yes":
                plan['loan_amount'] = car_loan_amount
                plan['loan_term'] = car_loan_term
                plan['loan_interest_rate'] = car_loan_interest_rate
                plan['loan_start_date'] = car_loan_start_date
                monthly_loan_payment, total_loan_payment = calculate_loan(car_loan_amount, car_loan_interest_rate, car_loan_term)
                plan['monthly_loan_payment'] = monthly_loan_payment
                plan['total_loan_payment'] = total_loan_payment
                plan['custom_loan_end_date'] = car_loan_start_date + pd.DateOffset(years=car_loan_term)

            for idx, p in enumerate(st.session_state['plans']):
                if p['name'] == "Buy a Car":
                    st.session_state['plans'][idx] = plan
                    break
            else:
                st.session_state['plans'].append(plan)

            st.write(f"To afford your dream car, you'll need to save: {currency_symbol}{monthly_savings_needed:.2f} each month")
            st.write(f"**Plan Name:** Buy a Car")
            st.write(f"**Target Amount:** {currency_symbol}{adjusted_car_price * (down_payment_percent / 100):,.2f}")
            st.write(f"**Monthly Savings Needed:** <span style='color: red;'>{currency_symbol}{monthly_savings_needed:,.2f}</span>", unsafe_allow_html=True)
            st.write(f"**Savings Term:** {(target_age - current_age) * 12} months")

            if take_car_loan == "Yes":
                st.write(f"**Monthly Car Loan Payment:** <span style='color: blue;'>{currency_symbol}{monthly_loan_payment:,.2f}</span>", unsafe_allow_html=True)
                st.write(f"**Total Car Loan Payment:** {currency_symbol}{total_loan_payment:,.2f}")

                amortization_schedule = calculate_amortization_schedule(car_loan_amount, car_loan_interest_rate, car_loan_term, pd.Timestamp(car_loan_start_date))

                # Plot the amortization schedule
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=amortization_schedule['Month'], y=amortization_schedule['Payment'].cumsum(), mode='lines', name='Payment', line=dict(color='brown')))
                fig.add_trace(go.Scatter(x=amortization_schedule['Month'], y=amortization_schedule['Interest'].cumsum(), mode='lines', name='Interest', line=dict(color='green')))
                fig.add_trace(go.Scatter(x=amortization_schedule['Month'], y=amortization_schedule['Balance'], mode='lines', name='Balance', line=dict(color='blue')))
                fig.update_layout(
                    title='Car Loan Amortization Schedule',
                    xaxis_title='Year',
                    yaxis_title=f'Amount ({currency_symbol})',
                    xaxis=dict(tickmode='linear', tick0=0, dtick=12),
                    showlegend=True
                )
                st.plotly_chart(fig)

# Retirement Savings Plan
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
            "name": "Retirement",
            "target_amount": amount_needed,
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

# Customized Financial Plan
if page == "Customized Financial Plan":
    st.title("Customized Financial Plan")

    # Inputs for custom financial plan
    plan_name = st.text_input("Enter the name of your plan:")
    plan_target_amount = st.number_input(f"Enter the target amount ({currency_symbol}):", min_value=0.0, format="%.2f")
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
                adjusted_target_amount = plan_target_amount - loan_amount
            else:
                adjusted_target_amount = plan_target_amount
            monthly_saving = calculate_monthly_saving(adjusted_target_amount, plan_current_savings, plan_current_savings_return, savings_term_months, inflation_rate)
            
            plan = {
                "name": plan_name,
                "target_amount": plan_target_amount,
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
            st.write(f"**Target Amount:** {currency_symbol}{plan_target_amount:,.2f}")
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