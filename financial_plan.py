import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime, timedelta, date
import matplotlib.pyplot as plt
from db import getUserPlans, getUserInfo, getTotalSavingsByYear, getPlan, getSavings, getTotalSavingsByMonth

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

# Custom color palette extracted from the provided image
custom_colors = [
    '#7FDBFF',  # Light blue
    '#2ECC40',  # Green
    '#39CCCC',  # Teal
    '#3D9970',  # Dark green
    '#FFDC00',  # Yellow
    '#FF851B',  # Orange
    '#FF4136',  # Red
    '#85144b',  # Maroon
    '#B10DC9',  # Purple
    '#F012BE',  # Pink
    '#001f3f',  # Navy
    '#0074D9',  # Blue
    '#7FDBFF',  # Aqua
    '#3D9970',  # Olive
    '#2ECC40',  # Lime
    '#01FF70'   # Bright green
    ]

def create_custom_legend(user_id, savings_distribution, custom_colors):
    profile = getUserInfo(user_id)
    st.markdown("   ")
    for i, (name, value) in enumerate(savings_distribution.items()):
        color = custom_colors[i % len(custom_colors)]
        st.markdown(
                f"<p style='color:{color};'><strong>{name}:</strong> {profile.user_currency}{value:,.2f}</p>", 
                unsafe_allow_html=True
        )

def display_piechart(user_id, savings_distribution):
    profile = getUserInfo(user_id)
    # Pie chart for savings distribution
    fig_pie = px.pie(
    values=list(savings_distribution.values()), 
    names=list(savings_distribution.keys()), 
    title='Monthly Savings Distribution', 
    hole=0.4
    )

    fig_pie.update_traces(
    textinfo='none', 
    insidetextorientation='radial',
    marker=dict(colors=custom_colors[:len(savings_distribution)])
    )

    fig_pie.update_layout(
    annotations=[dict(
        text=f'{sum(savings_distribution.values()):,.2f} {profile.user_currency}', 
        x=0.5, y=0.5, font_size=20, showarrow=False
    )],
    showlegend=False
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        st.plotly_chart(fig_pie)

    with col2:
        create_custom_legend(user_id, savings_distribution, custom_colors)

# Function to display the timeline
def display_timeline(user_id):
    plans = getUserPlans(user_id)
    events = []

    for plan in plans:
        end_date = plan.goal_date
        if isinstance(end_date, datetime):
            end_date = end_date.date()  # Convert to date if it's a datetime
        events.append({
            'event': plan.goal_name,
            'start_date': date.today(),
            'end_date': end_date
        })

    events_df = pd.DataFrame(events).sort_values(by='end_date')

    fig_timeline = go.Figure()
    for i, event in events_df.iterrows():
        fig_timeline.add_trace(go.Scatter(
            x=[event['end_date']],
            y=[1],
            mode='markers+text',
            name=event['event'],
            text=[f"{event['event']} - {event['end_date']}"],
            textposition=["top center"],
            marker=dict(color=custom_colors[i % len(custom_colors)], size=15)  # Increase marker size
        ))

    fig_timeline.update_layout(
        title='Timeline of Financial Goals',
        xaxis=dict(
            title='Year',
            tickformat='%Y',
            showticklabels=True,
            tickangle=-45
        ),
        yaxis=dict(
            showticklabels=False
        ),
        showlegend=False
        )
    
    st.plotly_chart(fig_timeline)

# Calculate mortization schedule
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

def filter_models(df, selected_make):
    models = df[df['make'] == selected_make]['model'].unique()
    return models

def calculate_car_savings(car_price, down_payment_percent, current_age, target_age, current_savings, current_savings_return, inflation_rate):
    down_payment = car_price * (down_payment_percent / 100)
    savings_timeframe_years = target_age - current_age
    savings_timeframe_months = savings_timeframe_years * 12
    monthly_savings_needed = calculate_monthly_saving(down_payment, current_savings, current_savings_return, savings_timeframe_months, inflation_rate)

    return float(monthly_savings_needed)

# Calculate mortgage payment
def calculate_loan_payment(loan_amount, annual_interest_rate, loan_term_years):
    monthly_interest_rate = annual_interest_rate / 100 / 12
    number_of_payments = loan_term_years * 12
    monthly_payment = np.abs(npf.pmt(monthly_interest_rate, number_of_payments, loan_amount))
    total_payment = monthly_payment * number_of_payments
    return float(monthly_payment)


# Define your function to create the graph
def generate_data_and_plot(plan_id, current_savings, savings_term_months, down_payment_amount, loan_term_years, monthly_saving, monthly_loan_payment, monthly_final_payment, currency_symbol):
    plan = getPlan(plan_id)
    savings_term_years = savings_term_months // 12
    yearly_saving = monthly_saving * 12
    yearly_loan_payment = monthly_loan_payment * 12
    yearly_final_payment = monthly_final_payment * 12

    # Generate data for plotting
    plan_year = plan.created_on.year
    total_years = max(savings_term_years + loan_term_years, 1)
    years = plan_year + np.arange(total_years)
    cumulative_savings = np.zeros(total_years, dtype=float)
    yearly_payments = np.zeros(total_years, dtype=float)
    actual_savings = np.zeros(total_years, dtype=float)

    # Get actual savings data by year
    total_savings_by_year = getTotalSavingsByYear(plan_id)

    # Initialize cumulative savings and actual savings for the first year
    if total_years > 0:
        yearly_payments[0] = yearly_saving if savings_term_years > 0 else 0
        cumulative_savings[0] = yearly_payments[0]
        actual_savings[0] = current_savings + total_savings_by_year.get(plan_year, 0)

    # Calculate cumulative savings and actual savings for subsequent years
    for i in range(1, savings_term_years):
        cumulative_savings[i] = cumulative_savings[i-1] + yearly_saving
        yearly_payments[i] = yearly_saving
        actual_savings[i] = actual_savings[i-1] + total_savings_by_year.get(plan_year + i, 0)
    savings_before_loan = cumulative_savings[range(savings_term_years)][-1] + yearly_loan_payment

    for i in range(savings_term_years, total_years):
        cumulative_savings[i] = savings_before_loan + (i - savings_term_years) * yearly_loan_payment
        yearly_payments[i] = yearly_loan_payment + yearly_final_payment
        actual_savings[i] = actual_savings[i - 1]  # Savings stop accumulating after the savings term

    data = pd.DataFrame({
        'Year': years,
        'Cumulative Savings': cumulative_savings,
        'Yearly Payments': yearly_payments,
        'Yearly Savings': yearly_saving,
        'Monthly Savings': monthly_saving,
        'Monthly Loan Payments': monthly_loan_payment,
        'Actual Savings': actual_savings
    })

    # Create the cumulative savings line plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['Year'],
        y=data['Cumulative Savings'],
        mode='lines+markers',
        name='Cumulative Savings',
        marker=dict(size=5),
        hovertemplate='Year: %{x}<br>Cumulative Savings: %{y:,.2f} ' + currency_symbol
    ))

    # Create the yearly payments bar plot
    fig.add_trace(go.Bar(
        x=data['Year'],
        y=data['Yearly Payments'],
        name='Yearly Payments',
        opacity=0.6,
        hovertemplate='Year: %{x}<br>Yearly Payments: %{y:,.2f} ' + currency_symbol
    ))

    # Create the actual savings line plot
    fig.add_trace(go.Scatter(
        x=data['Year'],
        y=data['Actual Savings'],
        mode='lines+markers',
        name='Actual Savings',
        marker=dict(size=5),
        line=dict(dash='dash'),
        hovertemplate='Year: %{x}<br>Actual Savings: %{y:,.2f} ' + currency_symbol
    ))

    fig.update_layout(
        title='Plan for Savings and Loan Payment',
        xaxis_title='Years',
        yaxis_title=f'Cumulative Savings ({currency_symbol})',
        legend_title='',
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=True
    )

    st.plotly_chart(fig)
    #st.write(data)

def generate_monthly_data_and_plot(plan_id, current_savings, savings_term_months, down_payment_amount, loan_term_years, monthly_saving, monthly_loan_payment, monthly_final_payment, currency_symbol):
    if savings_term_months > 12:
        st.error("Savings term months should be less than or equal to 12.")
        return

    plan = getPlan(plan_id)

    # Generate data for plotting
    plan_month = plan.created_on.month
    plan_year = plan.created_on.year
    total_months = savings_term_months + (loan_term_years * 12)
    months = [plan.created_on + pd.DateOffset(months=i) for i in range(total_months)]
    cumulative_savings = np.zeros(total_months, dtype=float)
    monthly_payments = np.zeros(total_months, dtype=float)
    actual_savings = np.zeros(total_months, dtype=float)

    # Get actual savings data by month
    total_savings_by_month = getTotalSavingsByMonth(plan_id)

    # Initialize cumulative savings and actual savings for the first month
    if total_months > 0:
        monthly_payments[0] = monthly_saving if savings_term_months > 0 else 0
        cumulative_savings[0] = monthly_payments[0]
        actual_savings[0] = current_savings + total_savings_by_month.get((plan_year, plan_month), 0)

    # Calculate cumulative savings and actual savings for subsequent months
    for i in range(1, savings_term_months):
        cumulative_savings[i] = cumulative_savings[i-1] + monthly_saving
        monthly_payments[i] = monthly_saving
        actual_savings[i] = actual_savings[i-1] + total_savings_by_month.get((plan_year, plan_month + i), 0)

    savings_before_loan = cumulative_savings[savings_term_months-1] + monthly_loan_payment

    for i in range(savings_term_months, total_months):
        cumulative_savings[i] = savings_before_loan + (i - savings_term_months) * monthly_loan_payment
        monthly_payments[i] = monthly_loan_payment + monthly_final_payment
        actual_savings[i] = actual_savings[i - 1]  # Savings stop accumulating after the savings term

    data = pd.DataFrame({
        'Month': months,
        'Cumulative Savings': cumulative_savings,
        'Monthly Payments': monthly_payments,
        'Monthly Savings': monthly_saving,
        'Monthly Loan Payments': monthly_loan_payment,
        'Actual Savings': actual_savings
    })

    # Create the cumulative savings line plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['Month'],
        y=data['Cumulative Savings'],
        mode='lines+markers',
        name='Cumulative Savings',
        marker=dict(size=5),
        hovertemplate='Month: %{x}<br>Cumulative Savings: %{y:,.2f} ' + currency_symbol
    ))

    # Create the monthly payments bar plot
    fig.add_trace(go.Bar(
        x=data['Month'],
        y=data['Monthly Payments'],
        name='Monthly Payments',
        opacity=0.6,
        hovertemplate='Month: %{x}<br>Monthly Payments: %{y:,.2f} ' + currency_symbol
    ))

    # Create the actual savings line plot
    fig.add_trace(go.Scatter(
        x=data['Month'],
        y=data['Actual Savings'],
        mode='lines+markers',
        name='Actual Savings',
        marker=dict(size=5),
        line=dict(dash='dash'),
        hovertemplate='Month: %{x}<br>Actual Savings: %{y:,.2f} ' + currency_symbol
    ))

    fig.update_layout(
        title='Plan for Savings and Loan Payment',
        xaxis_title='Months',
        yaxis_title=f'Cumulative Savings ({currency_symbol})',
        legend_title='',
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=True
    )

    st.plotly_chart(fig)

def create_savings_graph(plan_id):
    plan = getPlan(plan_id)
    savings = getSavings(plan.user_id, plan_id)

    if not plan or not savings:
        st.error("No data found for this specific plan.")
        return

    # Prepare data for the graph
    saving_dates = [saving.saving_date for saving in savings]
    actual_savings = [saving.saving_amount for saving in savings]

    # Create a DataFrame for actual savings
    df_savings = pd.DataFrame({
        'Date': saving_dates,
        'Actual Savings': actual_savings
    })

    # Ensure 'Date' column is in datetime format
    df_savings['Date'] = pd.to_datetime(df_savings['Date'])

    # Calculate expected savings
    start_date = min(saving_dates)
    end_date = plan.goal_date
    date_range = pd.date_range(start=start_date, end=end_date, freq='MS')
    expected_savings = [plan.goal_target_monthly for _ in range(len(date_range))]

    # Create a DataFrame for expected savings
    df_expected = pd.DataFrame({
        'Date': date_range,
        'Expected Savings': expected_savings
    })
    
    # Merge the dataframes on Date
    df = pd.merge(df_savings, df_expected, on='Date', how='outer').fillna(0)

    # Fill 'Expected Savings' where it is 0 with plan.goal_target_monthly
    df.loc[df['Expected Savings'] == 0, 'Expected Savings'] = plan.goal_target_monthly

    # Group by month and year
    df['Month'] = df['Date'].dt.to_period('M')
    df_grouped = df.drop(columns='Date').groupby('Month').sum().reset_index()

    # Convert 'Month' back to datetime for plotting
    df_grouped['Month'] = df_grouped['Month'].dt.to_timestamp()

    # Calculate the average of Expected Savings
    max_y_value = max(df_grouped['Expected Savings'].max(), df_grouped['Actual Savings'].max()) + 200

    # Set the minimum y-axis value to 0 or the minimum actual savings minus a margin
    min_y_value = min(df_grouped['Expected Savings'].min(), df_grouped['Actual Savings'].min()) - 200

    # Filter data to show only within the last and next 5 months
    current_date = datetime.now()
    past_date_limit = current_date - timedelta(days=5*30)  # approximately 5 months ago
    future_date_limit = current_date + timedelta(days=5*30)  # approximately 5 months from now

    df_filtered = df_grouped[(df_grouped['Month'] >= past_date_limit) & (df_grouped['Month'] <= future_date_limit)]

    # Create the plot with markers for each data point
    fig = px.line(df_filtered, x='Month', y=['Actual Savings', 'Expected Savings'],
                  title='Savings Comparison',
                  labels={'value': 'Amount', 'variable': 'Legend'},
                  markers=True)

    # Update the y-axis range
    fig.update_yaxes(range=[min_y_value, max_y_value])

    st.plotly_chart(fig)

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
