#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st

# 页面标题
st.title("Recommended Investment Options for High Risk and Long Term")

# 描述
st.write("Based on your high risk tolerance and preference for long-term investments, we recommend the following options:")

# 推荐的投资选项
st.subheader("1. Individual Stocks")
st.write("""
Investing in individual stocks can offer substantial returns over the long term.
Selecting a diversified portfolio of high-growth companies can maximize returns but comes with higher risk.
- **Typical Duration**: 10 years or more
- **Expected Return**: High, but with significant risk
""")

st.subheader("2. Real Estate Investments")
st.write("""
Directly investing in real estate properties can provide high returns through property value appreciation and rental income.
This option requires active management and carries higher risk.
- **Typical Duration**: 10 years or more
- **Expected Return**: High, with high risk and capital requirements
""")

st.subheader("3. Venture Capital and Private Equity")
st.write("""
Investing in venture capital and private equity involves providing capital to startups and private companies with high growth potential.
These investments can offer significant returns but come with very high risk.
- **Typical Duration**: 10 years or more
- **Expected Return**: Very high, but with very high risk
""")

st.subheader("4. High-Growth Mutual Funds/ETFs")
st.write("""
High-growth mutual funds and ETFs invest in companies with high growth potential.
These funds are diversified but can be volatile.
- **Typical Duration**: 10 years or more
- **Expected Return**: High, with higher volatility
""")

# 返回按钮
if st.button("Back to Assessment"):
    st.switch_page("pages/7_risktolerance.py")

