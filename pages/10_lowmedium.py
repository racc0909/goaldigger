#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st

# 页面标题
st.title("Recommended Investment Options for Low Risk and Medium Term")

# 描述
st.write("Based on your low risk tolerance and preference for medium-term investments, we recommend the following options:")

# 推荐的投资选项
st.subheader("1. Intermediate-Term Government Bonds")
st.write("""
Intermediate-term Government Bonds, such as Treasury Notes (T-notes), are debt securities issued by the government.
They offer regular interest payments over a fixed period and are considered very safe.
- **Typical Duration**: 2 to 10 years
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
For medium-term, consider CDs with longer terms.
- **Typical Duration**: 1 to 5 years
- **Expected Return**: Higher than regular savings accounts, and can be quite attractive over medium terms
""")

st.subheader("4. Corporate Bonds (High-Grade)")
st.write("""
High-grade Corporate Bonds are debt securities issued by financially stable companies.
They offer regular interest payments over a fixed period.
- **Typical Duration**: 2 to 10 years
- **Expected Return**: Moderate, with low to moderate risk
""")

# 返回按钮
if st.button("Back to Assessment"):
    st.session_state.page = "Risk Tolerance Assessment"

