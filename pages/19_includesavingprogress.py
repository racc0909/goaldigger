import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime, date
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Custom color palette extracted from the provided image
custom_colors = ['#7FDBFF', '#2ECC40', '#39CCCC', '#3D9970', '#FFDC00']

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
page = st.sidebar.radio("Go to", ["Overview", "House Buyer Savings Plan", "Car Buyer Savings Plan", "Retirement Savings Plan", "Customized Financial Plan", "Track Your Savings Progress"])

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

# Helper function to calculate loan payments and total payments
def calculate_loan(loan_amount, annual_interest_rate, loan_term_years):
    monthly_interest_rate = annual_interest_rate / 100 / 12
    number_of_payments = loan_term_years * 12
    monthly_payment = np.abs(npf.pmt(monthly_interest_rate, number_of_payments, loan_amount))
    total_payment = monthly_payment * number_of_payments
    return monthly_payment, total_payment

# Function to calculate amortization schedule
def calculate_amortization_schedule(loan_amount, annual_interest_rate, loan_term_years, start_date):
    monthly_interest_rate = annual_interest_rate / 100 / 12
    number_of_payments = loan_term_years * 12
    monthly_payment = np.abs(npf.pmt(monthly_interest_rate, number_of_payments, loan_amount))

    schedule = []
    balance = loan_amount
    for i in range(number_of_payments):
        interest = balance * monthly_interest_rate
        principal = monthly_payment - interest
        balance -= principal
        if balance < 0:
            balance = 0
        schedule.append({
            'Month': start_date + pd.DateOffset(months=i),
            'Payment': monthly_payment,
            'Principal': principal,
            'Interest': interest,
            'Balance': balance
        })
    return pd.DataFrame(schedule)

# Handle plan deletion
def handle_deletion():
    query_params = st.experimental_get_query_params()
    if 'delete_plan' in query_params:
        delete_idx = int(query_params['delete_plan'][0])
        del st.session_state['plans'][delete_idx]
        st.experimental_rerun()

# Function to display the timeline
def display_timeline():
    events = []
    for plan in st.session_state['plans']:
        events.append({
            'name': plan['name'],
            'end_date': plan['due_date'].date() if isinstance(plan['due_date'], datetime) else plan['due_date'],
            'icon': 'car' if 'car' in plan['name'].lower() else 'house' if 'house' in plan['name'].lower() else 'retirement' if 'retirement' in plan['name'].lower() else 'custom'
        })

    events_df = pd.DataFrame(events).sort_values(by='end_date')

    fig = go.Figure()
    for idx, row in events_df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['end_date']],
            y=[0.5],
            mode='markers+text',
            marker=dict(size=20, symbol='circle', color='blue'),
            text=row['name'],
            textposition='bottom center'
        ))
        icon_path = ''
        if row['icon'] == 'car':
            icon_path = r'C:\Users\thaon\OneDrive\Documents\BFA\FIWP\icon\carloan.png'
        elif row['icon'] == 'house':
            icon_path = '/mnt/data/file-VnPOC45ZbATmShZ0cWL5JO6d'
        elif row['icon'] == 'retirement':
            icon_path = 'https://path.to/your/retirement_icon.png'
        else:
            icon_path = 'https://path.to/your/custom_icon.png'
        fig.add_layout_image(
            dict(
                source=icon_path,
                xref="x",
                yref="y",
                x=row['end_date'],
                y=1.1,
                sizex=0.1,
                sizey=0.1,
                xanchor="center",
                yanchor="middle"
            )
        )

    fig.update_layout(
        title='Timeline of Financial Goals',
        xaxis_title='Date',
        yaxis=dict(showticklabels=False),
        showlegend=False,
        height=300
    )

# Function to filter plans based on the selected date range
def filter_plans_by_date(plans, selected_month):
    filtered_plans = []
    for plan in plans:
        plan_due_date = plan['due_date'] if isinstance(plan['due_date'], datetime) else datetime.combine(plan['due_date'], datetime.min.time())
        if plan_due_date >= selected_month:
            filtered_plans.append(plan)
        if 'monthly_loan_payment' in plan:
            loan_start_date = plan['loan_start_date'].date() if isinstance(plan['loan_start_date'], datetime) else plan['loan_start_date']
            loan_end_date = loan_start_date + timedelta(days=plan['loan_term']*365)
            if loan_start_date <= selected_month.date() <= loan_end_date:
                if plan not in filtered_plans:
                    filtered_plans.append(plan)
    return filtered_plans

# Overview page
if page == "Overview":
    st.title(f"Overview of All Financial Plans for {user_name}")

    if st.session_state['plans']:

        # Rearrange plans
        plan_order = st.multiselect("Drag to reorder plans", options=[plan['name'] for plan in st.session_state['plans']], default=[plan['name'] for plan in st.session_state['plans']])
        st.session_state['plans'] = [plan for name in plan_order for plan in st.session_state['plans'] if plan['name'] == name]

        # Date selection
        selected_date = st.date_input("Select month and year to view savings distribution", date.today(), min_value=date.today())

        # Filter plans based on the selected date
        filtered_plans = []
        for plan in st.session_state['plans']:
            due_date = plan['due_date'].date() if isinstance(plan['due_date'], datetime) else plan['due_date']
            if due_date >= selected_date:
                filtered_plans.append(plan)

         # Calculate savings distribution
        total_monthly_savings = sum(plan['monthly_saving'] for plan in filtered_plans)
        savings_distribution = {plan['name']: plan['monthly_saving'] for plan in filtered_plans}

        # Adding loan/mortgage amounts to savings distribution
        total_monthly_loans = sum(plan['monthly_loan_payment'] for plan in filtered_plans if 'monthly_loan_payment' in plan)
        if total_monthly_loans > 0:
            savings_distribution['Loans/Mortgages'] = total_monthly_loans

        # Calculate the total amount
        total_amount = total_monthly_savings + total_monthly_loans

        # Generate color mapping for plans
        color_mapping = {plan['name']: custom_colors[i % len(custom_colors)] for i, plan in enumerate(st.session_state['plans'])}
        if 'Loans/Mortgages' in savings_distribution:
            color_mapping['Loans/Mortgages'] = custom_colors[len(st.session_state['plans']) % len(custom_colors)]

        col1, col2 = st.columns([2, 1])

        with col1:
            # Pie chart for savings distribution
            fig_pie = px.pie(values=list(savings_distribution.values()), names=list(savings_distribution.keys()), title='Monthly Savings Distribution', hole=0.4, color_discrete_sequence=[color_mapping[name] for name in savings_distribution.keys()])
            fig_pie.update_traces(textinfo='label+percent', insidetextorientation='radial')
            fig_pie.update_layout(
                annotations=[dict(text=f'{currency_symbol}{total_amount:,.2f}', x=0.5, y=0.5, font_size=20, showarrow=False)],
                showlegend=True
            )
            st.plotly_chart(fig_pie)

        # Graph for total savings over time
        savings_data = {'Date': [], 'Total Savings': []}
        start_date = datetime.today()
        end_date = max(plan['due_date'] if isinstance(plan['due_date'], datetime) else datetime.combine(plan['due_date'], datetime.min.time()) for plan in st.session_state['plans'])
        current_date = start_date

        while current_date <= end_date:
            current_monthly_savings = sum(plan['monthly_saving'] for plan in filter_plans_by_date(st.session_state['plans'], current_date))
            savings_data['Date'].append(current_date)
            savings_data['Total Savings'].append(current_monthly_savings)
            current_date += timedelta(days=30)  # Move to next month

        savings_df = pd.DataFrame(savings_data)

        fig_savings = go.Figure()
        fig_savings.add_trace(go.Scatter(x=savings_df['Date'], y=savings_df['Total Savings'], mode='lines+markers', name='Total Savings'))
        fig_savings.update_layout(
            title='Total Savings Over Time',
            xaxis_title='Date',
            yaxis_title=f'Total Savings ({currency_symbol})',
            xaxis=dict(tickmode='linear', dtick="M12", tickformat="%Y"),
            showlegend=True,
            height=300
        )
        st.plotly_chart(fig_savings)



        # Display the timeline of financial goals with matching colors
        events = []
        for plan in st.session_state['plans']:
            events.append({
                'name': plan['name'],
                'end_date': plan['due_date'].date() if isinstance(plan['due_date'], datetime) else plan['due_date'],
                'color': custom_colors[plan_order.index(plan['name']) % len(custom_colors)] if plan['name'] in plan_order else custom_colors[len(events) % len(custom_colors)]
            })

        events_df = pd.DataFrame(events).sort_values(by='end_date')

        fig = go.Figure()
        for idx, row in events_df.iterrows():
            fig.add_trace(go.Scatter(
                x=[row['end_date']],
                y=[0.5],
                mode='markers+text',
                marker=dict(size=20, symbol='circle', color=row['color']),
                text=row['name'],
                textposition='bottom center'
            ))

        fig.update_layout(
            title='Timeline of Financial Goals',
            xaxis_title='Date',
            yaxis=dict(showticklabels=False),
            showlegend=False,
            height=300
        )
        st.plotly_chart(fig)

        # Plans with loans
        st.subheader(" Saving Plans Summary")
        col1, col2 = st.columns(2)
        for i, plan in enumerate([p for p in st.session_state['plans'] if 'monthly_loan_payment' in p]):      
            with col1 if i % 2 == 0 else col2:
                st.markdown(
                    f"""
                    <div id="wholetext" style="background-color:#f4f4f4; padding: 10px; margin: 10px; border-radius: 10px;">
                        <div class="plan-box">
                            <h3>{plan['name']}</h3>
                            <p><strong>Target Amount:</strong> {currency_symbol}{plan['target_amount']:,.2f}</p>
                            <p><strong>Due Date:</strong> {plan['due_date'].strftime('%Y-%m-%d')}</p>
                            <p style='color: red;'><strong>Monthly Savings needed:</strong> {currency_symbol}{plan['monthly_saving']:,.2f}</p>
                            <div style='background-color:#e0f7fa; padding: 10px; border-radius: 10px;'>
                                <p style='color: blue;'><strong>Monthly Savings needed for Loan Payment:</strong> {currency_symbol}{plan['monthly_loan_payment']:,.2f}</p>
                                <p><strong>Total Loan Payment:</strong> {currency_symbol}{plan['total_loan_payment']:,.2f}</p>
                                <p><strong>Loan End Date:</strong> {plan['loan_start_date'].strftime('%Y-%m-%d')} to {(plan['loan_start_date'] + pd.DateOffset(years=plan['loan_term'])).strftime('%Y-%m-%d')}</p>
                            </div>
                            <a href="?page={plan['details_link']}">{plan['details_link']}</a>
                            <form action="?delete_plan={i}" method="post">
                                <button type="submit" class="delete-button" style="background-color: red; color: white; border: none; padding: 5px 10px; cursor: pointer;">Delete</button>
                            </form>
                        </div>
                    </div>
                    """, unsafe_allow_html=True
                )

        # Plans without loans
        st.subheader("")
        col1, col2 = st.columns(2)
        for i, plan in enumerate([p for p in st.session_state['plans'] if 'monthly_loan_payment' not in p]):
            with col1 if i % 2 == 0 else col2:
                st.markdown(
                    f"""
                    <div id="wholetext" style="background-color:#f4f4f4; padding: 10px; margin: 10px; border-radius: 10px;">
                        <div class="plan-box">
                            <h3>{plan['name']}</h3>
                            <p><strong>Target Amount:</strong> {currency_symbol}{plan['target_amount']:,.2f}</p>
                            <p><strong>Due Date:</strong> {plan['due_date'].strftime('%Y-%m-%d')}</p>
                            <p style="color: red;"><strong>Monthly Savings needed:</strong> {currency_symbol}{plan['monthly_saving']:,.2f}</p>
                            <a href="?page={plan['details_link']}">{plan['details_link']}</a>
                            <form action="?delete_plan={i}" method="post">
                                <button type="submit" class="delete-button" style="background-color: red; color: white; border: none; padding: 5px 10px; cursor: pointer;">Delete</button>
                            </form>
                        </div>
                    </div>
                    """, unsafe_allow_html=True
                )

    else:
        st.write("No financial plans found. Please add a plan first.")
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

            if take_house_loan == "Yes":
                st.write(f"**Monthly Mortgage Payment:** <span style='color: blue;'>{currency_symbol}{monthly_loan_payment:,.2f}</span>", unsafe_allow_html=True)
                st.write(f"**Total Mortgage Payment:** {currency_symbol}{total_loan_payment:,.2f}")

                amortization_schedule = calculate_amortization_schedule(mortgage_loan_amount, mortgage_interest_rate, mortgage_loan_term, pd.Timestamp(mortgage_start_date))

                # Plot the amortization schedule
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=amortization_schedule['Month'], y=amortization_schedule['Payment'].cumsum(), mode='lines', name='Payment', line=dict(color='brown')))
                fig.add_trace(go.Scatter(x=amortization_schedule['Month'], y=amortization_schedule['Interest'].cumsum(), mode='lines', name='Interest', line=dict(color='green')))
                fig.add_trace(go.Scatter(x=amortization_schedule['Month'], y=amortization_schedule['Balance'], mode='lines', name='Balance', line=dict(color='blue')))
                fig.update_layout(
                    title='Mortgage Amortization Schedule',
                    xaxis_title='Year',
                    yaxis_title=f'Amount ({currency_symbol})',
                    xaxis=dict(tickmode='linear', dtick="M12", tickformat="%Y"),
                    showlegend=True
                )
                st.plotly_chart(fig)

                st.subheader("Your Local Mortgage Providers")
                ads = [
                    {
                        "company": "Your German Mortgage",
                        "description": "We have been assisting Expats for more than 20 years to secure their German mortgage. An easy English speaking step-by-step service which is free of charge. Blue-Card holders welcome. Five star Google Reviews from our clients prove our services.",
                        "link_text": "View more",
                        "link": "https://www.yourgermanmortgage.com"
                    },
                    {
                        "company": "Baufi24",
                        "description": "Baufi24 is Germany’s first digital mortgage broker. Baufi24 combines smart technology and certified mortgage advice to help clients save time and money while making property purchasing in Germany transparent and hassle-free.",
                        "link_text": "View more",
                        "link": "https://www.baufi24.de"
                    },
                    {
                        "company": "Hypofriend",
                        "description": "Hypofriend is Germany’s smartest mortgage broker, built by PhDs and engineers they calculate the optimal mortgage for your situation. Their English-speaking mortgage experts will guide you through the entire process giving you insights along the way, free of charge.",
                        "link_text": "View more",
                        "link": "https://www.hypofriend.de"
                    },
                    {
                        "company": "finbird.digital",
                        "description": "finbird digital provides English mortgage and property consulting for international professionals throughout Germany. We help with checking your property budget and affordability at an early stage and with guiding you along the purchase process until transaction close. We educate about the buying process and mortgage financing options with recurring events and comprehensive educational guides.",
                        "link_text": "View more",
                        "link": "https://www.finbird.digital"
                    }
                ]

                col1, col2 = st.columns(2)
                for i, ad in enumerate(ads):
                    with col1 if i % 2 == 0 else col2:
                        st.markdown(f"""
                        <div style="background-color:#f4f4f4; padding: 10px; margin: 10px; border-radius: 10px;">
                            <h3>{ad['company']}</h3>
                            <p>{ad['description']}</p>
                            <a href="{ad['link']}" target="_blank">{ad['link_text']}</a>
                        </div>
                        """, unsafe_allow_html=True)
# Car Buyer Savings Plan
if page == "Car Buyer Savings Plan":
    st.title("Car Buyer Savings Plan")

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

    def calculate_car_savings(car_price, down_payment_percent, current_age, target_age, current_savings, current_savings_return, inflation_rate):
        down_payment = car_price * (down_payment_percent / 100)
        savings_timeframe_years = target_age - current_age
        savings_timeframe_months = savings_timeframe_years * 12
        monthly_savings_needed = calculate_monthly_saving(down_payment, current_savings, current_savings_return, savings_timeframe_months, inflation_rate)
        return monthly_savings_needed

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

    def calculate_loan(loan_amount, annual_interest_rate, loan_term_years):
        monthly_interest_rate = annual_interest_rate / 100 / 12
        number_of_payments = loan_term_years * 12
        monthly_payment = np.abs(npf.pmt(monthly_interest_rate, number_of_payments, loan_amount))
        total_payment = monthly_payment * number_of_payments
        return monthly_payment, total_payment

    def calculate_amortization_schedule(loan_amount, annual_interest_rate, loan_term_years, start_date):
        monthly_interest_rate = annual_interest_rate / 100 / 12
        number_of_payments = loan_term_years * 12
        monthly_payment = np.abs(npf.pmt(monthly_interest_rate, number_of_payments, loan_amount))

        schedule = []
        balance = loan_amount
        for i in range(number_of_payments):
            interest = balance * monthly_interest_rate
            principal = monthly_payment - interest
            balance -= principal
            if balance < 0:
                balance = 0
            schedule.append({
                'Month': start_date + pd.DateOffset(months=i),
                'Payment': monthly_payment,
                'Principal': principal,
                'Interest': interest,
                'Balance': balance
            })
        return pd.DataFrame(schedule)

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

# Helper function to get a list of years
def get_years(start_year, end_year):
    return [str(year) for year in range(start_year, end_year + 1)]

# Track Your Savings Progress page
if page == "Track Your Savings Progress":
    st.title("Track Your Savings Progress")

    # Month and Year selection
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    years = get_years(2020, datetime.now().year + 10)
    col1, col2 = st.columns([2, 1])
    selected_month = col1.selectbox ("Select month", months, index=datetime.now().month - 1)
    selected_year = col2.selectbox("Select year", years, index=years.index(str(datetime.now().year)))
    
    # Convert selected month and year to date
    selected_date = datetime.strptime(f"01 {selected_month} {selected_year}", "%d %B %Y")

    if 'actual_savings' not in st.session_state:
        st.session_state['actual_savings'] = {}

    if 'actual_loan_payments' not in st.session_state:
        st.session_state['actual_loan_payments'] = {}

    # Function to filter plans based on the selected date range
    def filter_plans_by_date(plans, selected_month):
        filtered_plans = []
        for plan in plans:
            plan_due_date = plan['due_date'] if isinstance(plan['due_date'], datetime) else datetime.combine(plan['due_date'], datetime.min.time())
            if plan_due_date >= selected_month:
                filtered_plans.append(plan)
        return filtered_plans

    # Filter plans based on the selected date
    filtered_plans = filter_plans_by_date(st.session_state['plans'], selected_date)

    if filtered_plans:
        total_actual_savings = 0

        for plan in filtered_plans:
            st.subheader(f"Plan: {plan['name']}")

            # Input for actual savings
            actual_savings_key = f'actual_savings_{plan["name"]}'
            if actual_savings_key not in st.session_state:
                st.session_state[actual_savings_key] = []

            actual_savings = st.number_input(f"Enter your actual savings for {plan['name']} in {selected_month} {selected_year} ({currency_symbol}):", min_value=0.0, step=0.01, key=f'input_{actual_savings_key}')
            st.session_state[actual_savings_key].append(actual_savings)
            total_actual_savings_for_plan = sum(st.session_state[actual_savings_key])

            with st.expander(f"Details for {plan['name']}", expanded=False):
                st.write(f"Total Actual Savings for {plan['name']}: {currency_symbol}{total_actual_savings_for_plan:,.2f}")
                st.write(f"Target Amount for {plan['name']}: {currency_symbol}{plan['target_amount']:,.2f}")

                if plan['target_amount'] > 0:
                    progress = min(total_actual_savings_for_plan / plan['target_amount'], 1.0)
                    st.progress(progress)

                    if total_actual_savings_for_plan < plan['target_amount']:
                        st.markdown(f"<a href='https://www.investopedia.com/articles/pf/07/money_management.asp' target='_blank'>How to make your money grow</a>", unsafe_allow_html=True)
                    else:
                        st.success("You did well!")
                else:
                    st.warning("Target amount for this plan is zero, cannot calculate progress.")

            total_actual_savings += actual_savings

        # Store the actual savings for the selected month
        st.session_state['actual_savings'][selected_date.strftime('%Y-%m')] = total_actual_savings

    # Combined Loan/Mortgage Section
    st.subheader(f"Loan/Mortgage Payments")

    # Input for total loan/mortgage payments
    actual_loan_payment_key = f'actual_loan_payment_total'
    if actual_loan_payment_key not in st.session_state:
        st.session_state[actual_loan_payment_key] = []

    actual_loan_payment = st.number_input(f"Enter your total actual loan/mortgage payment in {selected_month} {selected_year} ({currency_symbol}):", min_value=0.0, step=0.01, key=f'input_{actual_loan_payment_key}')
    st.session_state[actual_loan_payment_key].append(actual_loan_payment)
    total_actual_loan_payments = sum(st.session_state[actual_loan_payment_key])

    total_expected_loan_payments = sum(plan['monthly_loan_payment'] for plan in st.session_state['plans'] if 'monthly_loan_payment' in plan)
    
    with st.expander(f"Details for Loan/Mortgage Payments", expanded=False):
        st.write(f"Total Actual Loan/Mortgage Payments: {currency_symbol}{total_actual_loan_payments:,.2f}")
        st.write(f"Expected Monthly Loan/Mortgage Payments: {currency_symbol}{total_expected_loan_payments:,.2f}")

        if total_expected_loan_payments > 0:
            loan_progress = min(total_actual_loan_payments / total_expected_loan_payments, 1.0)
            st.progress(loan_progress)

            if total_actual_loan_payments < total_expected_loan_payments:
                st.markdown(f"<a href='https://www.investopedia.com/articles/pf/07/money_management.asp' target='_blank'>How to make your money grow</a>", unsafe_allow_html=True)
            else:
                st.success("You did well!")
        else:
            st.warning("Expected monthly loan/mortgage payments are zero, cannot calculate progress.")

    # Store the actual loan payments for the selected month
    st.session_state['actual_loan_payments'][selected_date.strftime('%Y-%m')] = total_actual_loan_payments

    # Graph the actual savings against the expected savings
    dates = sorted(set(st.session_state['actual_savings'].keys()).union(set(st.session_state['actual_loan_payments'].keys())))
    actual_savings_values = [sum(st.session_state['actual_savings'].get(date, 0) + st.session_state['actual_loan_payments'].get(date, 0) for date in dates[:i+1]) for i in range(len(dates))]
    expected_savings_values = []

    for date in dates:
        date_obj = datetime.strptime(date, '%Y-%m')
        filtered_plans_for_date = filter_plans_by_date(st.session_state['plans'], date_obj)
        expected_savings_for_date = sum(plan['monthly_saving'] for plan in filtered_plans_for_date)
        expected_loan_payments_for_date = sum(plan['monthly_loan_payment'] for plan in filtered_plans_for_date if 'monthly_loan_payment' in plan)
        expected_savings_values.append(expected_savings_for_date + expected_loan_payments_for_date)

    # Accumulate the expected savings over time
    expected_savings_values = [sum(expected_savings_values[:i+1]) for i in range(len(expected_savings_values))]

    savings_df = pd.DataFrame({
        'Date': [datetime.strptime(date, '%Y-%m') for date in dates],
        'Actual Savings': actual_savings_values,
        'Expected Savings': expected_savings_values
    })

    fig_savings = go.Figure()
    fig_savings.add_trace(go.Scatter(x=savings_df['Date'], y=savings_df['Actual Savings'], mode='lines+markers', name='Actual Savings'))
    fig_savings.add_trace(go.Scatter(x=savings_df['Date'], y=savings_df['Expected Savings'], mode='lines+markers', name='Expected Savings'))
    fig_savings.update_layout(
        title='Actual Savings vs. Expected Savings Over Time',
        xaxis_title='Date',
        yaxis_title=f'Savings ({currency_symbol})',
        xaxis=dict(tickmode='linear', dtick="M1", tickformat="%Y-%m"),
        showlegend=True,
        height=400
    )
    st.plotly_chart(fig_savings)