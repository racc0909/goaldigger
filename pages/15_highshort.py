#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st

# 页面标题
st.title("Recommended Investment Options for High Risk and Short Term")

# 描述
st.write("Based on your high risk tolerance and preference for short-term investments, we recommend the following options:")

# 推荐的投资选项
st.subheader("1. Individual Stocks")
st.write("""
Investing in individual stocks can offer high returns in a short period, but also comes with higher risk.
Short-term trading can be very volatile.
- **Typical Duration**: Less than 1 year
- **Expected Return**: High, but with significant risk
""")

st.subheader("2. Options Trading")
st.write("""
Options trading allows investors to speculate on the price movement of stocks.
While it can offer high returns, it also carries a high risk of loss.
- **Typical Duration**: Days to months
- **Expected Return**: Very high, but with very high risk
""")

st.subheader("3. Cryptocurrencies")
st.write("""
Cryptocurrencies are highly volatile digital assets that can offer substantial returns over short periods.
They are suitable for investors who can tolerate extreme price swings.
- **Typical Duration**: Days to months
- **Expected Return**: Very high, but with very high risk
""")

st.subheader("4. Leveraged ETFs")
st.write("""
Leveraged ETFs aim to amplify the returns of an underlying index. They are designed for short-term trading and can be very volatile.
- **Typical Duration**: Days to weeks
- **Expected Return**: High, but with high risk and volatility
""")

# 返回按钮
if st.button("Back to Assessment"):
    st.switch_page("pages/7_risktolerance.py")

