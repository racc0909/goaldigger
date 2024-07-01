#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


# In[ ]:


# Investment Options Comparison Calculator Page
st.title("Investment Options Comparison Calculator")
st.write("Enter your investment amount and term to simulate the expected returns on different investment options.")

# 利率信息
cd_rates = {
    '1_year': 0.0434,  # 4.34%
    '3_year': 0.03,    # 假设为3.0%
    '5_year': 0.035    # 假设为3.5%
}

gov_bond_rates = {
    '1_year': 0.015,  # 1.5%
    '3_year': 0.02,   # 2.0%
    '5_year': 0.025   # 2.5%
}

money_market_rates = {
    '1_year': 0.0065,  # 0.65%
    '3_year': 0.01,    # 假设为1.0%
    '5_year': 0.015    # 假设为1.5%
}

investment_amount = st.number_input("Investment Amount (€)", min_value=0, value=125000)
investment_term = st.selectbox("Investment Term (Years)", [1, 3, 5])

def calculate_return(amount, years, rate):
    return amount * (1 + rate) ** years

if st.button("Calculate"):
    term_str = f'{investment_term}_year'
    cd_return = calculate_return(investment_amount, investment_term, cd_rates[term_str])
    gov_bond_return = calculate_return(investment_amount, investment_term, gov_bond_rates[term_str])
    money_market_return = calculate_return(investment_amount, investment_term, money_market_rates[term_str])
    
    st.write(f"Expected return after {investment_term} years:")
    st.write(f"Certificate of Deposit (CD): {cd_return:.2f} €")
    st.write(f"Government Bonds: {gov_bond_return:.2f} €")
    st.write(f"Money Market Funds: {money_market_return:.2f} €")
    
    # 图表展示
    terms = [1, 3, 5]
    cd_returns = [calculate_return(investment_amount, term, cd_rates[f'{term}_year']) for term in terms]
    gov_bond_returns = [calculate_return(investment_amount, term, gov_bond_rates[f'{term}_year']) for term in terms]
    money_market_returns = [calculate_return(investment_amount, term, money_market_rates[f'{term}_year']) for term in terms]

    plt.figure(figsize=(10, 6))
    plt.plot(terms, cd_returns, marker='o', label='Certificate of Deposit (CD)')
    plt.plot(terms, gov_bond_returns, marker='o', label='Government Bonds')
    plt.plot(terms, money_market_returns, marker='o', label='Money Market Funds')
    plt.title("Investment Returns Over Different Terms")
    plt.xlabel("Investment Term (Years)")
    plt.ylabel("Expected Return (€)")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

