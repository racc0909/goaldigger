import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime, timedelta, date
import matplotlib.pyplot as plt

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
    return float(monthly_saving)

# Handle plan deletion: todo
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
        end_date = plan['due_date']
        if isinstance(end_date, datetime):
            end_date = end_date.date()  # Convert to date if it's a datetime
        events.append({
            'event': plan['name'],
            'start_date': date.today(),
            'end_date': end_date
        })

    events_df = pd.DataFrame(events).sort_values(by='end_date')

    fig_timeline = go.Figure()
    for _, event in events_df.iterrows():
        fig_timeline.add_trace(go.Scatter(
            x=[event['end_date']],
            y=[1],
            mode='markers+text',
            name=event['event'],
            text=[f"{event['event']} - {event['end_date']}"],
            textposition='top center'
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

# Calculate mortgage payment
def calculate_mortgage_payment(loan_amount, annual_interest_rate, loan_term_years):
    monthly_interest_rate = annual_interest_rate / 100 / 12
    number_of_payments = loan_term_years * 12
    monthly_payment = np.abs(npf.pmt(monthly_interest_rate, number_of_payments, loan_amount))
    total_payment = monthly_payment * number_of_payments
    return float(monthly_payment), float(total_payment)

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

    return monthly_savings_needed

def calculate_car_loan(loan_amount, annual_interest_rate, loan_term_years):
    monthly_interest_rate = annual_interest_rate / 100 / 12
    number_of_payments = loan_term_years * 12
    monthly_payment = np.abs(npf.pmt(monthly_interest_rate, number_of_payments, loan_amount))
    total_payment = monthly_payment * number_of_payments
    return float(monthly_payment), float(total_payment)

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

def calculate_loan(loan_amount, annual_interest_rate, loan_term_years):
        monthly_interest_rate = annual_interest_rate / 100 / 12
        number_of_payments = loan_term_years * 12
        monthly_payment = np.abs(npf.pmt(monthly_interest_rate, number_of_payments, loan_amount))
        total_payment = monthly_payment * number_of_payments
        return monthly_payment, total_payment