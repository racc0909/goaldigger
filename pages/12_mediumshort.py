#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st

# 页面标题
st.title("Recommended Investment Options for Medium Risk and Short Term")

# 描述
st.write("Based on your medium risk tolerance and preference for short-term investments, we recommend the following options:")

# 推荐的投资选项
st.subheader("1. Corporate Bonds (Investment-Grade)")
st.write("""
Investment-grade corporate bonds are issued by financially stable companies and offer higher returns than government bonds.
They come with moderate risk and are suitable for short-term investments.
- **Typical Duration**: 1 to 3 years
- **Expected Return**: Moderate, with relatively low risk compared to lower-grade corporate bonds
""")

st.subheader("2. Balanced Mutual Funds")
st.write("""
Balanced mutual funds invest in a mix of stocks and bonds, aiming to balance risk and return.
They are less volatile than pure equity funds and suitable for short-term investment horizons.
- **Typical Duration**: 1 to 3 years
- **Expected Return**: Moderate, with a balanced risk profile
""")

st.subheader("3. Short-term Bond Funds")
st.write("""
Short-term bond funds invest in bonds with short maturities, reducing interest rate risk.
They offer higher returns than money market funds but come with moderate risk.
- **Typical Duration**: 1 to 3 years
- **Expected Return**: Moderate, with lower risk than longer-term bond funds
""")

st.subheader("4. Dividend-Paying Stocks")
st.write("""
Dividend-paying stocks provide regular income through dividends and potential for capital appreciation.
They can be more volatile than bonds but offer higher returns.
- **Typical Duration**: 1 to 3 years
- **Expected Return**: Moderate to high, with moderate risk
""")

# 返回按钮
if st.button("Back to Assessment"):
    st.switch_page("pages/7_risktolerance.py")

