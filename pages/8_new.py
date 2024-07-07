import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime, date

# Initialize session state for plans if not already set
if 'plans' not in st.session_state:
    st.session_state['plans'] = []

# Helper function to calculate current age from birthdate
def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, today.day))

# Personal Information
st.sidebar.header('Personal Info')
user_name = st.sidebar.text_input('What is your name?')
birthdate = st.sidebar.date_input('When is your birthday?', min_value=date(1900, 1, 1), max_value=date.today())
current_age = calculate_age(birthdate)

inflation_rate = st.sidebar.slider('Annual inflation rate (%)', min_value=0.0, max_value=10.0, value=2.0, step=0.1, key='annual_inflation_rate')
currency = st.sidebar.selectbox('Select your currency:', ['USD', 'EUR', 'GBP'], key='currency')

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

# Helper function to calculate monthly savings
def calculate_monthly_saving(target_amount, current_savings, current_savings_return, savings_term_months, inflation_rate):
    # Adjust the target amount for inflation
    future_value_target_amount = target_amount * ((1 + inflation_rate / 100) ** (savings_term_months / 12))

    monthly_interest_rate = current_savings_return / 100 / 12
    number_of_payments = savings_term_months
    if current_savings > 0:
        current_savings_future_value = current_savings * ((1 + monthly_interest_rate) ** number_of_payments)
        future_value_needed = future_value_target_amount - current_savings_future_value
    else:
        future_value_needed = future_value_target_amount
    if future_value_needed <= 0:
        return 0
    monthly_saving = npf.pmt(monthly_interest_rate, number_of_payments, 0, -future_value_needed)
    return monthly_saving

# Handle plan deletion
def handle_deletion():
    query_params = st.experimental_get_query_params()
    if 'delete_plan' in query_params:
        delete_idx = int(query_params['delete_plan'][0])
        del st.session_state['plans'][delete_idx]
        st.experimental_rerun()
# Function to display the timeline
def display_timeline():
    plans = st.session_state['plans']
    events = []
    for plan in plans:
        events.append({
            'name': plan['name'],
            'end_date': plan['due_date'],
            'details': f"{plan['name']} - {plan['due_date'].strftime('%Y')}"
        })
    
    if 'Buy a House' in [p['name'] for p in plans]:
        house_plan = next(p for p in plans if p['name'] == 'Buy a House')
        mortgage_end_date = house_plan['due_date'] + pd.DateOffset(years=house_plan['savings_term_months'] // 12)
        events.append({
            'name': 'Mortgage End',
            'end_date': mortgage_end_date,
            'details': f"Mortgage End - {mortgage_end_date.strftime('%Y')}"
        })

    events_df = pd.DataFrame(events).sort_values(by='end_date')

    fig = go.Figure()
    for index, row in events_df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['end_date']],
            y=[1],
            mode='markers+text',
            name=row['name'],
            text=row['details'],
            textposition='bottom center'
        ))

    fig.update_layout(
        title='Timeline of Financial Goals',
        xaxis_title='Year',
        yaxis_title='Events',
        yaxis=dict(showticklabels=False),
        showlegend=False,
        height=300
    )
    st.plotly_chart(fig)

# Overview page
if page == "Overview":
    st.title(f"Overview of All Financial Plans for {user_name}")

    if st.session_state['plans']:
        total_monthly_savings = sum(plan['monthly_saving'] for plan in st.session_state['plans'])
        savings_distribution = {plan['name']: plan['monthly_saving'] for plan in st.session_state['plans']}

        # Rearrange plans
        st.subheader("Rearrange Plans")
        plan_order = st.multiselect("Drag to reorder plans", options=[plan['name'] for plan in st.session_state['plans']], default=[plan['name'] for plan in st.session_state['plans']])
        st.session_state['plans'] = [plan for name in plan_order for plan in st.session_state['plans'] if plan['name'] == name]

        col1, col2 = st.columns([2, 1])

        with col1:

            # Plotting the timeline of financial goals
            display_timeline()
	  
            # Pie chart for savings distribution
            fig_pie = px.pie(values=list(savings_distribution.values()), names=list(savings_distribution.keys()), title='Monthly Savings Distribution')
            st.plotly_chart(fig_pie)

        col1, col2 = st.columns(2)
        for i, plan in enumerate(st.session_state['plans']):
            with col1 if i % 2 == 0 else col2:
                st.markdown(f"""
                <div style="background-color:#f4f4f4; padding: 10px; margin: 10px; border-radius: 10px;">
                    <h3>{plan['name']}</h3>
                    <p><strong>Target Amount:</strong> {currency_symbol}{plan['target_amount']:,.2f}</p>
                    <p><strong>Due Date:</strong> {plan['due_date'].strftime('%Y-%m-%d')}</p>
                    <p style="color: red;"><strong>Monthly Savings Needed:</strong> {currency_symbol}{plan['monthly_saving']:,.2f}</p>
                    <p><strong>Savings Term:</strong> {plan['savings_term_months']} months</p>
                    <a href="?page={plan['details_link']}">{plan['details_link']}</a>
                    <form action="?delete_plan={i}" method="post">
                        <button type="submit" style="background-color: red; color: white; border: none; padding: 5px 10px; cursor: pointer;">Delete</button>
                    </form>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.write("No financial plans found. Please add a plan first.")

# House Buyer Savings Plan
if page == "House Buyer Savings Plan":
    st.title("House Buyer Savings Plan")

    option = st.radio("Select Option", ["Savings Plan", "Mortgage Calculator"])
    house_price = st.number_input(f'House price ({currency_symbol}):', min_value=0.0, format="%.2f", key='house_price')
    house_down_payment_percent = st.slider('Down payment percentage:', min_value=0.0, max_value=100.0, step=0.1, format="%.1f", key='house_down_payment_percent')

    if option == "Savings Plan":
        house_target_age = st.number_input("Enter the age by which you want to achieve this goal:", min_value=current_age + 1, max_value=100, step=1, key='house_target_age')
        house_current_savings = st.number_input(f'Current savings for the house ({currency_symbol}, optional):', min_value=0.0, format="%.2f", key='house_current_savings')

        house_current_savings_return = 0
        if house_current_savings > 0:
            house_current_savings_return = st.slider('Annual return on current savings (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='house_current_savings_return')

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
                for idx, p in enumerate(st.session_state['plans']):
                    if p['name'] == "Buy a House":
                        st.session_state['plans'][idx] = plan
                        break
                else:
                    st.session_state['plans'].append(plan)
                
                st.write(f"**Plan Name:** Buy a House")
                st.write(f"**Target Amount:** {currency_symbol}{house_price * (house_down_payment_percent / 100):,.2f}")
                st.write(f"**Monthly Savings Needed:** <span style='color: red;'>{currency_symbol}{monthly_saving:,.2f}</span>", unsafe_allow_html=True)
                st.write(f"**Savings Term:** {savings_term_months} months")

    if option == "Mortgage Calculator":
        house_price_float = float(house_price)  # Ensure house_price is a float
        down_payment_amount = house_price_float * (house_down_payment_percent / 100)
        mortgage_loan_amount = st.number_input(f'Mortgage loan amount ({currency_symbol}):', min_value=0.0, format="%.2f", value=0.0 if house_price == 0 else house_price_float - down_payment_amount)
        mortgage_interest_rate = st.slider('Mortgage interest rate (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='mortgage_interest_rate')
        mortgage_loan_term = st.number_input('Mortgage loan term (years):', min_value=1, max_value=30, step=1, key='mortgage_loan_term')
        mortgage_start_date = st.date_input("Mortgage start date:", min_value=date.today(), key='mortgage_start_date')

        def calculate_mortgage_payment(loan_amount, annual_interest_rate, loan_term_years):
            monthly_interest_rate = annual_interest_rate / 100 / 12
            number_of_payments = loan_term_years * 12
            monthly_payment = np.abs(npf.pmt(monthly_interest_rate, number_of_payments, loan_amount))
            return monthly_payment

        if st.button('Calculate Mortgage Payment'):
            monthly_mortgage_payment = calculate_mortgage_payment(mortgage_loan_amount, mortgage_interest_rate, mortgage_loan_term)
            st.write(f"**Monthly Mortgage Payment:** {currency_symbol}{monthly_mortgage_payment:,.2f}")

            st.write("### See Your Local Rates")
            ads = [
                {
                    "company": "District Lending",
                    "apr": "6.352%",
                    "payment": f"{currency_symbol}1,971 /mo",
                    "rate": "6.250%",
                    "fees_points": f"{currency_symbol}3,459",
                    "includes_points": f"Includes 0.831 Points ({currency_symbol}2,659)",
                    "nmls": "#1835285",
                    "link": "https://www.districtlending.com"
                },
                {
                    "company": "OwnUp",
                    "apr": "6.594%",
                    "payment": f"{currency_symbol}2,023 /mo",
                    "rate": "6.500%",
                    "fees_points": f"{currency_symbol}3,128",
                    "includes_points": f"Includes 0.750 Points ({currency_symbol}2,400)",
                    "nmls": "#12007",
                    "link": "https://www.ownup.com"
                },
                {
                    "company": "Nation Home Loans",
                    "apr": "6.691%",
                    "payment": f"{currency_symbol}2,023 /mo",
                    "rate": "6.500%",
                    "fees_points": f"{currency_symbol}6,626",
                    "includes_points": f"Includes 0.600 Points ({currency_symbol}1,920)",
                    "nmls": "#1513908",
                    "link": "https://www.nationhomeloans.com"
                },
                {
                    "company": "TOMO Mortgage",
                    "apr": "6.768%",
                    "payment": f"{currency_symbol}2,049 /mo",
                    "rate": "6.625%",
                    "fees_points": f"{currency_symbol}4,752",
                    "includes_points": f"Includes 0.860 Points ({currency_symbol}2,752)",
                    "nmls": "#2059741",
                    "link": "https://www.tomomortgage.com"
                }
            ]
            col1, col2 = st.columns(2)
            for i, ad in enumerate(ads):
                with col1 if i % 2 == 0 else col2:
                    st.markdown(f"""
                    <div style="background-color:#f4f4f4; padding: 10px; margin: 10px; border-radius: 10px;">
                        <h3>{ad['company']}</h3>
                        <p><strong>APR:</strong> {ad['apr']}</p>
                        <p><strong>Payment:</strong> {ad['payment']}</p>
                        <p><strong>Rate:</strong> {ad['rate']}</p>
                        <p><strong>Fees & Points:</strong> {ad['fees_points']}</p>
                        <p><strong>Includes Points:</strong> {ad['includes_points']}</p>
                        <p><strong>NMLS:</strong> {ad['nmls']}</p>
                        <a href="{ad['link']}" target="_blank">Apply Now</a>
                    </div>
                    """, unsafe_allow_html=True)
# Car Buyer Savings Plan
if page == "Car Buyer Savings Plan":
    st.title("Car Buyer Savings Plan")

    option = st.radio("Select Option", ["Savings Plan", "Car Loan Calculator"])

    @st.cache_data
    def load_car_data(file_path):
        try:
            df = pd.read_excel(file_path)
            return df
        except FileNotFoundError:
            st.error(f"File '{file_path}' not found. Please check the file path.")
            st.stop()

    def filter_models(df, selected_make):
        models = df[df['make'] == selected_make]['model'].unique()
        return models

    def calculate_car_savings(car_price, down_payment_percent, current_age, target_age, current_savings, current_savings_return):
        down_payment = car_price * (down_payment_percent / 100)
        savings_timeframe_years = target_age - current_age
        savings_timeframe_months = savings_timeframe_years * 12
        monthly_savings_needed = calculate_monthly_saving(down_payment, current_savings, current_savings_return, savings_timeframe_months, inflation_rate)

        return monthly_savings_needed

    def calculate_car_loan(loan_amount, annual_interest_rate, loan_term_years):
        monthly_interest_rate = annual_interest_rate / 100 / 12
        number_of_payments = loan_term_years * 12
        monthly_payment = npf.pmt(monthly_interest_rate, number_of_payments, loan_amount)
        return monthly_payment

    file_path = "C:/Users/thaon/OneDrive/Documents/BFA/FIWP/car_prices.xlsx"
    df = load_car_data(file_path)

    if option == "Savings Plan":
        st.header('Choose an Option:')
        savings_option = st.radio('', ('See Available Suggested Car Prices', 'Input Your Car Price'))

        if savings_option == 'See Available Suggested Car Prices':
            st.subheader('See Available Suggested Car Prices')

            selected_make = st.selectbox('Select Car Make', df['make'].unique())

            if selected_make:
                models = filter_models(df, selected_make)
                selected_model = st.selectbox('Select Car Model', models)

                if selected_model:
                    selected_car_details = df[(df['make'] == selected_make) & (df['model'] == selected_model)]
                    full_name = selected_car_details['make'].values[0] + ' ' + selected_car_details['model'].values[0]
                    price = selected_car_details['sellingprice'].values[0]
                    st.write(f"Full Name: {full_name}")
                    st.write(f"Suggested price: {currency_symbol}{price:.2f}")

                    adjusted_car_price = st.number_input('Adjust the car price if needed:', min_value=0.0, format="%.2f", value=float(price), key='adjusted_car_price')
                    down_payment_percent = st.slider('Enter your down payment percentage:', min_value=0.0, max_value=100.0, step=1.0, key='car_down_payment_percent')
                    target_age = st.number_input('Enter the age you wish to buy the car:', value=30, min_value=0, max_value=100, step=1, key='car_target_age')
                    car_current_savings = st.number_input(f'Current savings for the car ({currency_symbol}, optional):', min_value=0.0, format="%.2f", key='car_current_savings')

                    car_current_savings_return = 0
                    if car_current_savings > 0:
                        car_current_savings_return = st.slider('Annual return on current savings (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='car_current_savings_return')

                    if st.button('Calculate Car Plan'):
                        if target_age <= current_age:
                            st.error("The target age must be greater than the current age.")
                        else:
                            monthly_savings_needed = calculate_car_savings(
                                adjusted_car_price, down_payment_percent, current_age, target_age, car_current_savings, car_current_savings_return)

                            plan = {
                                "name": "Buy a Car",
                                "target_amount": adjusted_car_price * (down_payment_percent / 100),
                                "due_date": datetime.now().replace(year=datetime.now().year + (target_age - current_age)),
                                "monthly_saving": monthly_savings_needed,
                                "savings_term_months": (target_age - current_age) * 12,
                                "details_link": "Car Buyer Savings Plan"
                            }
                            for idx, p in enumerate(st.session_state['plans']):
                                if p['name'] == "Buy a Car":
                                    st.session_state['plans'][idx] = plan
                                    break
                            else:
                                st.session_state['plans'].append(plan)

                            st.write(f"To afford your dream car, you'll need to save: {currency_symbol}{monthly_savings_needed:.2f} each month")

        elif savings_option == 'Input Your Car Price':
            st.subheader('Input Your Car Price')

            car_price_input = st.number_input('Enter the total cost of the car:', value=0.0, min_value=0.0, step=1000.0, format="%.2f")

            down_payment_percent = st.slider('Enter your down payment percentage:', min_value=0.0, max_value=100.0, step=1.0, key='car_down_payment_percent')
            target_age = st.number_input('Enter the age you wish to buy the car:', value=30, min_value=0, max_value=100, step=1, key='car_target_age')
            car_current_savings = st.number_input(f'Current savings for the car ({currency_symbol}, optional):', min_value=0.0, format="%.2f", key='car_current_savings')

            car_current_savings_return = 0
            if car_current_savings > 0:
                car_current_savings_return = st.slider('Annual return on current savings (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='car_current_savings_return')

            if st.button('Calculate Car Plan'):
                if target_age <= current_age:
                    st.error("The target age must be greater than the current age.")
                else:
                    monthly_savings_needed = calculate_car_savings(
                        car_price_input, down_payment_percent, current_age, target_age, car_current_savings, car_current_savings_return)

                    plan = {
                        "name": "Buy a Car",
                        "target_amount": car_price_input * (down_payment_percent / 100),
                        "due_date": datetime.now().replace(year=datetime.now().year + (target_age - current_age)),
                        "monthly_saving": monthly_savings_needed,
                        "savings_term_months": (target_age - current_age) * 12,
                        "details_link": "Car Buyer Savings Plan"
                    }
                    for idx, p in enumerate(st.session_state['plans']):
                        if p['name'] == "Buy a Car":
                            st.session_state['plans'][idx] = plan
                            break
                    else:
                        st.session_state['plans'].append(plan)

                    st.write(f"To afford your dream car, you'll need to save: {currency_symbol}{monthly_savings_needed:.2f} each month")

    if option == "Car Loan Calculator":
        st.subheader("Car Loan Calculator")

        loan_amount = st.number_input(f'Loan amount ({currency_symbol}):', min_value=0.0, format="%.2f", key='car_loan_amount')
        loan_interest_rate = st.slider('Loan interest rate (%):', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='car_loan_interest_rate')
        loan_term_years = st.number_input('Loan term (years):', min_value=0, max_value=30, step=1, key='car_loan_term_years')

        if st.button('Calculate Loan Payment'):
            monthly_loan_payment = calculate_car_loan(loan_amount, loan_interest_rate, loan_term_years)
            st.write(f"**Monthly Loan Payment:** {currency_symbol}{monthly_loan_payment:,.2f}")

            amortization_schedule = calculate_amortization_schedule(loan_amount, loan_interest_rate, loan_term_years, pd.Timestamp(datetime.now()))

            st.write("### Amortization Schedule")
            st.dataframe(amortization_schedule)

            # Plot the amortization schedule
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=amortization_schedule['Month'], y=amortization_schedule['Principal'], mode='lines', name='Principal'))
            fig.add_trace(go.Scatter(x=amortization_schedule['Month'], y=amortization_schedule['Interest'], mode='lines', name='Interest'))
            fig.add_trace(go.Scatter(x=amortization_schedule['Month'], y=amortization_schedule['Balance'], mode='lines', name='Balance'))
            fig.update_layout(
                title='Car Loan Amortization Schedule',
                xaxis_title='Month',
                yaxis_title=f'Amount ({currency_symbol})',
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

    def calculate_pension_monthly_saving(target_amount, current_savings, current_savings_return, savings_term_years):
        monthly_interest_rate = current_savings_return / 100 / 12
        number_of_payments = savings_term_years * 12
        if current_savings > 0:
            future_value_needed = target_amount - current_savings * ((1 + monthly_interest_rate) ** number_of_payments)
        else:
            future_value_needed = target_amount
        if future_value_needed <= 0:
            return 0
        monthly_saving = npf.pmt(monthly_interest_rate, number_of_payments, 0, -future_value_needed)
        return monthly_saving

    if st.button('Calculate Retirement Plan'):
        pension_target_date = datetime.now().replace(year=datetime.now().year + (retirement_age - current_age))
        current_date = datetime.now().date()
        savings_term_years = retirement_age - current_age
        monthly_saving = calculate_pension_monthly_saving(amount_needed, current_savings, pension_current_savings_return, savings_term_years)
        
        plan = {
            "name": "Retirement Savings Plan",
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

    if st.button('Calculate Custom Plan'):
        current_date = datetime.now().date()
        if plan_target_date <= current_date:
            st.error("Target date must be in the future.")
        else:
            savings_term_months = (plan_target_date.year - current_date.year) * 12 + (plan_target_date.month - current_date.month)
            monthly_saving = calculate_monthly_saving(plan_target_amount, plan_current_savings, plan_current_savings_return, savings_term_months, inflation_rate)
            
            plan = {
                "name": plan_name,
                "target_amount": plan_target_amount,
                "due_date": plan_target_date,
                "monthly_saving": monthly_saving,
                "savings_term_months": savings_term_months,
                "details_link": "Customized Financial Plan"
            }
            st.session_state['plans'].append(plan)
            
            st.write(f"**Plan Name:** {plan_name}")
            st.write(f"**Target Amount:** {currency_symbol}{plan_target_amount:,.2f}")
            st.write(f"**Monthly Savings Needed:** <span style='color: red;'>{currency_symbol}{monthly_saving:,.2f}</span>", unsafe_allow_html=True)
            st.write(f"**Savings Term:** {savings_term_months} months")

            # Calculate savings growth timeline
            savings_growth = []
            monthly_interest_rate = plan_current_savings_return / 100 / 12

            for month in range(savings_term_months + 1):
                if month == 0:
                    savings_growth.append(plan_current_savings)
                else:
                    savings_growth.append(savings_growth[-1] * (1 + monthly_interest_rate) + monthly_saving)

            savings_growth_months = savings_growth
            months = pd.date_range(start=current_date, periods=savings_term_months + 1, freq='M').strftime('%Y-%m')

            # Plot savings growth
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=months, y=savings_growth_months, mode='lines+markers', name='Savings Growth', line=dict(color='blue')))
            fig.update_layout(
                title=f'Savings Growth Over Time for {plan_name}',
                xaxis_title='Month',
                yaxis_title=f'Total Savings ({currency_symbol})',
                showlegend=True
            )
            st.plotly_chart(fig)