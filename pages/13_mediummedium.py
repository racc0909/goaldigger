#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st

# 页面标题
st.title("Recommended Investment Options for Medium Risk and Medium Term")

# 描述
st.write("Based on your medium risk tolerance and preference for medium-term investments, we recommend the following options:")

# 推荐的投资选项
st.subheader("1. Balanced Mutual Funds")
st.write("""
Balanced mutual funds invest in a mix of stocks and bonds, aiming to balance risk and return.
They provide moderate returns and are less volatile than pure equity funds.
- **Typical Duration**: 3 to 5 years
- **Expected Return**: Moderate, with a balanced risk profile
""")

st.subheader("2. Corporate Bonds (Investment-Grade)")
st.write("""
Investment-grade corporate bonds are issued by financially stable companies and offer higher returns than government bonds.
They are suitable for medium-term investments with moderate risk.
- **Typical Duration**: 3 to 5 years
- **Expected Return**: Moderate, with relatively low risk compared to lower-grade corporate bonds
""")

st.subheader("3. Dividend-Paying Stocks")
st.write("""
Dividend-paying stocks provide regular income through dividends and potential for capital appreciation.
They offer higher returns than bonds and are suitable for medium-term investment horizons.
- **Typical Duration**: 3 to 5 years
- **Expected Return**: Moderate to high, with moderate risk
""")

st.subheader("4. Real Estate Investment Trusts (REITs)")
st.write("""
REITs allow you to invest in real estate without directly owning property.
They often provide high dividends and have the potential for appreciation.
- **Typical Duration**: 3 to 5 years
- **Expected Return**: Moderate to high, with moderate risk
""")

# 返回按钮
if st.button("Back to Assessment"):
    st.session_state.page = "Risk Tolerance Assessment"

