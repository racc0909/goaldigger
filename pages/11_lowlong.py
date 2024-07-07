#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st

# 页面标题
st.title("Recommended Investment Options for Low Risk and Long Term")

# 描述
st.write("Based on your low risk tolerance and preference for long-term investments, we recommend the following options:")

# 推荐的投资选项
st.subheader("1. Government Bonds")
st.write("""
Government Bonds, especially long-term bonds, are debt securities issued by the government.
They offer regular interest payments over a fixed period and are considered very safe.
- **Typical Duration**: 10 to 30 years
- **Expected Return**: Low to moderate, but very safe
""")

st.subheader("2. High-Yield Savings Accounts")
st.write("""
High-Yield Savings Accounts offer higher interest rates than regular savings accounts while maintaining liquidity and safety.
They are suitable for those who want to keep their funds accessible.
- **Typical Duration**: No fixed duration, accessible anytime
- **Expected Return**: Higher than regular savings accounts, but lower than CDs
""")

st.subheader("3. Certificates of Deposit (CDs)")
st.write("""
Certificates of Deposit (CDs) are low-risk savings products offered by banks and credit unions.
They offer a fixed interest rate for a specified term, making them a predictable and secure investment option.
For long-term, consider CDs with longer terms.
- **Typical Duration**: 5 to 10 years
- **Expected Return**: Higher than regular savings accounts, and can be quite attractive over long terms
""")

st.subheader("4. Municipal Bonds")
st.write("""
Municipal Bonds are debt securities issued by states, municipalities, or counties to finance public projects.
They are often exempt from federal taxes, and sometimes state and local taxes as well.
- **Typical Duration**: 10 to 30 years
- **Expected Return**: Moderate, with low risk and tax advantages
""")

# 返回按钮
if st.button("Back to Assessment"):
    st.session_state.page = "Risk Tolerance Assessment"

