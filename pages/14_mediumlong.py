#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st

# 页面标题
st.title("Recommended Investment Options for Medium Risk and Long Term")

# 描述
st.write("Based on your medium risk tolerance and preference for long-term investments, we recommend the following options:")

# 推荐的投资选项
st.subheader("1. Diversified Stock Portfolios")
st.write("""
Investing in a diversified portfolio of stocks can offer substantial returns over the long term.
Diversification helps manage risk while aiming for growth.
- **Typical Duration**: 5 to 10 years or more
- **Expected Return**: Moderate to high, with moderate risk
""")

st.subheader("2. Real Estate Investment Trusts (REITs)")
st.write("""
REITs allow you to invest in real estate without directly owning property.
They often provide high dividends and have the potential for appreciation.
- **Typical Duration**: 5 to 10 years
- **Expected Return**: Moderate to high, with moderate risk
""")

st.subheader("3. Balanced Mutual Funds")
st.write("""
Balanced mutual funds invest in a mix of stocks and bonds, aiming to balance risk and return.
They provide moderate returns and are less volatile than pure equity funds.
- **Typical Duration**: 5 to 10 years
- **Expected Return**: Moderate, with a balanced risk profile
""")

st.subheader("4. Corporate Bonds (Investment-Grade)")
st.write("""
Investment-grade corporate bonds are issued by financially stable companies and offer higher returns than government bonds.
They are suitable for long-term investments with moderate risk.
- **Typical Duration**: 5 to 10 years
- **Expected Return**: Moderate, with relatively low risk compared to lower-grade corporate bonds
""")

# 返回按钮
if st.button("Back to Assessment"):
    st.switch_page("pages/7_risktolerance.py")

