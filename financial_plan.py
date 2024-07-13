import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime, timedelta, date
import matplotlib.pyplot as plt
from db import getUserPlans

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

# Calculate mortgage payment
def calculate_loan_payment(loan_amount, annual_interest_rate, loan_term_years):
    monthly_interest_rate = annual_interest_rate / 100 / 12
    number_of_payments = loan_term_years * 12
    monthly_payment = np.abs(npf.pmt(monthly_interest_rate, number_of_payments, loan_amount))
    total_payment = monthly_payment * number_of_payments
    return float(monthly_payment)

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


# Define your function to create the graph
def generate_data_and_plot(current_savings, savings_term_months, down_payment_amount, loan_term_years, monthly_saving, monthly_loan_payment, currency_symbol):
    savings_term_years = savings_term_months // 12
    yearly_saving = monthly_saving * 12
    yearly_loan_payment = monthly_loan_payment * 12

    # Generate data for plotting
    years = np.arange(savings_term_years + loan_term_years)
    cumulative_savings = np.zeros_like(years, dtype=float)
    yearly_payments = np.zeros_like(years, dtype=float)

    for i in range(savings_term_years):
        cumulative_savings[i] = current_savings + i * yearly_saving
        yearly_payments[i] = yearly_saving

    for i in range(savings_term_years, len(years)):
        cumulative_savings[i] = down_payment_amount + (i - savings_term_years) * yearly_loan_payment
        yearly_payments[i] = yearly_loan_payment

    data = pd.DataFrame({
        'Year': years,
        'Cumulative Savings': cumulative_savings,
        'Yearly Payments': yearly_payments,
        'Yearly Savings': np.where(years < savings_term_years, yearly_saving, np.nan),
        'Monthly Savings': np.where(years < savings_term_years, monthly_saving, np.nan),
        'Monthly Loan Payments': np.where(years >= savings_term_years, monthly_loan_payment, np.nan)
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

    fig.update_layout(
        title='Savings and Mortgage Plan',
        xaxis_title='Years',
        yaxis_title=f'Cumulative Savings ({currency_symbol})',
        legend_title='',
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=True
    )

    st.plotly_chart(fig)