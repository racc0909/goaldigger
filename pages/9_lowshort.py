#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st

# 页面标题
st.title("Recommended Investment Options for Low Risk and Short Term")

# 描述
st.write("Based on your low risk tolerance and preference for short-term investments, we recommend the following options:")

# 推荐的投资选项
st.subheader("1. Money Market Funds")
st.write("""
Money Market Funds invest in short-term, high-quality securities issued by government and corporate entities. 
They offer low risk and high liquidity, making them suitable for short-term investment goals.
- **Typical Duration**: A few months to a year
- **Expected Return**: Low, but stable
""")

st.subheader("2. Certificates of Deposit (CDs)")
st.write("""
Certificates of Deposit (CDs) are low-risk savings products offered by banks and credit unions. 
They offer a fixed interest rate for a specified term, making them a predictable and secure investment option.
- **Typical Duration**: 3 months to 1 year
- **Expected Return**: Higher than regular savings accounts
""")

st.subheader("3. Short-term Government Bonds")
st.write("""
Short-term Government Bonds, such as Treasury Bills (T-bills), are debt securities issued by the government. 
They offer regular interest payments over a fixed period and are considered very safe.
- **Typical Duration**: 4 weeks to 1 year
- **Expected Return**: Low, but very safe
""")

st.subheader("4. High-Yield Savings Accounts")
st.write("""
High-Yield Savings Accounts offer higher interest rates than regular savings accounts while maintaining liquidity and safety.
- **Typical Duration**: No fixed duration, accessible anytime
- **Expected Return**: Higher than regular savings accounts, but lower than CDs
""")

# 返回按钮
if st.button("Back to Assessment"):
    st.session_state.page = "Risk Tolerance Assessment"

