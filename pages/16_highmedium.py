#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st

# 页面标题
st.title("Recommended Investment Options for High Risk and Medium Term")

# 描述
st.write("Based on your high risk tolerance and preference for medium-term investments, we recommend the following options:")

# 推荐的投资选项
st.subheader("1. Individual Stocks")
st.write("""
Investing in individual stocks can offer high returns, but also comes with higher risk.
Diversifying your stock portfolio can help manage risk.
- **Typical Duration**: 3 to 5 years
- **Expected Return**: High, but with significant risk
""")

st.subheader("2. Real Estate Investment Trusts (REITs)")
st.write("""
REITs allow you to invest in real estate without directly owning property.
They often provide high dividends and have the potential for appreciation.
- **Typical Duration**: 3 to 7 years
- **Expected Return**: Moderate to high, with moderate risk
""")

st.subheader("3. High-Yield Corporate Bonds (Junk Bonds)")
st.write("""
High-yield corporate bonds, also known as junk bonds, offer higher returns than investment-grade bonds but come with higher risk.
They are issued by companies with lower credit ratings.
- **Typical Duration**: 2 to 5 years
- **Expected Return**: High, but with higher risk
""")

st.subheader("4. Mutual Funds/ETFs with Aggressive Growth")
st.write("""
Mutual funds and ETFs that focus on aggressive growth invest in companies with high growth potential.
These funds are diversified but can be volatile.
- **Typical Duration**: 3 to 5 years
- **Expected Return**: High, but with higher volatility
""")

# 返回按钮
if st.button("Back to Assessment"):
    st.switch_page("pages/7_risktolerance.py")

