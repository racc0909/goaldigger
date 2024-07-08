#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st

# 页面标题
st.title("Recommended Investment Options for Low Risk and Medium Term")

# 描述
st.write("Based on your low risk tolerance and preference for medium-term investments, we recommend the following options:")

# 自定义CSS样式
st.markdown("""
    <style>
    .custom-box {
        border: 2px solid #cccccc;
        border-radius: 10px;
        padding: 15px;
        margin: 10px;
        transition: all 0.3s ease-in-out;
    }
    .custom-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# 推荐的投资选项
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="custom-box">
        <h2>1. Intermediate-Term Government Bonds</h2>
        <p>
        Intermediate-term Government Bonds, such as Treasury Notes (T-notes), are debt securities issued by the government. 
        They offer regular interest payments over a fixed period and are considered very safe.
        <ul>
            <li><b>Typical Duration</b>: 2 to 10 years</li>
            <li><b>Expected Return</b>: Low to moderate, but very safe</li>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="custom-box">
        <h2>2. High-Yield Savings Accounts</h2>
        <p>
        High-Yield Savings Accounts offer higher interest rates than regular savings accounts while maintaining liquidity and safety.
        They are suitable for those who want to keep their funds accessible.
        <ul>
            <li><b>Typical Duration</b>: No fixed duration, accessible anytime</li>
            <li><b>Expected Return</b>: Higher than regular savings accounts, but lower than CDs</li>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="custom-box">
        <h2>3. Certificates of Deposit (CDs)</h2>
        <p>
        Certificates of Deposit (CDs) are low-risk savings products offered by banks and credit unions. 
        They offer a fixed interest rate for a specified term, making them a predictable and secure investment option.
        For medium-term, consider CDs with longer terms.
        <ul>
            <li><b>Typical Duration</b>: 1 to 5 years</li>
            <li><b>Expected Return</b>: Higher than regular savings accounts, and can be quite attractive over medium terms</li>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="custom-box">
        <h2>4. Corporate Bonds (High-Grade)</h2>
        <p>
        High-grade Corporate Bonds are debt securities issued by financially stable companies.
        They offer regular interest payments over a fixed period.
        <ul>
            <li><b>Typical Duration</b>: 2 to 10 years</li>
            <li><b>Expected Return</b>: Moderate, with low to moderate risk</li>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

# 返回按钮
if st.button("Back to Assessment"):
    st.switch_page("pages/7_risktolerance.py")

