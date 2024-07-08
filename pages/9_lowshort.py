#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st

# 页面标题
st.title("Recommended Investment Options for Low Risk and Short Term")

# 描述
st.write("Based on your low risk tolerance and preference for short-term investments, we recommend the following options:")

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
        <h2>1. Money Market Funds</h2>
        <p>
        Money Market Funds invest in short-term, high-quality securities issued by government and corporate entities. 
        They offer low risk and high liquidity, making them suitable for short-term investment goals.
        <ul>
            <li><b>Typical Duration</b>: A few months to a year</li>
            <li><b>Expected Return</b>: Low, but stable</li>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="custom-box">
        <h2>2. Short-term Government Bonds</h2>
        <p>
        Short-term Government Bonds, such as Treasury Bills (T-bills), are debt securities issued by the government. 
        They offer regular interest payments over a fixed period and are considered very safe.
        <ul>
            <li><b>Typical Duration</b>: 4 weeks to 1 year</li>
            <li><b>Expected Return</b>: Low, but very safe</li>
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
        <ul>
            <li><b>Typical Duration</b>: 3 months to 1 year</li>
            <li><b>Expected Return</b>: Higher than regular savings accounts</li>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
with col4:
    st.markdown("""
    <div class="custom-box">
        <h2>4. High-Yield Savings Accounts</h2>
        <p>
        High-Yield Savings Accounts offer higher interest rates than regular savings accounts while maintaining liquidity and safety.
        <ul>
            <li><b>Typical Duration</b>: No fixed duration, accessible anytime</li>
            <li><b>Expected Return</b>: Higher than regular savings accounts, but lower than CDs</li>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

# 返回按钮
if st.button("Back to Assessment"):
    st.switch_page("pages/7_risktolerance.py")

