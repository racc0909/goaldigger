#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st

# 页面标题
st.title("Recommended Investment Options for High Risk and Short Term")

# 描述
st.write("Based on your high risk tolerance and preference for short-term investments, we recommend the following options:")

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
    .duration-bar, .return-bar {
        height: 10px;
        border-radius: 5px;
        margin-top: 5px;
        margin-left: 20px; /* 缩进与项目符号对齐 */
    }
    .duration-bar {
        background-color: #4CAF50; /* 绿色 */
    }
    .return-bar {
        background-color: #2196F3; /* 蓝色 */
    }
    </style>
    """, unsafe_allow_html=True)

# 推荐的投资选项
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="custom-box">
        <h2>1. Leveraged ETFs</h2>
        <p>
        Leveraged ETFs aim to amplify the returns of an underlying index. They are designed for short-term trading and can be very volatile.
        <ul>
            <li><b>Typical Duration</b>: Days to weeks</li>
            <div class="duration-bar" style="width: 10%;"></div>
            <li><b>Expected Return</b>: High, but with high risk and volatility</li>
            <div class="return-bar" style="width: 80%;"></div>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="custom-box">
        <h2>2. Options Trading</h2>
        <p>
        Options trading allows investors to speculate on the price movement of stocks.
        While it can offer high returns, it also carries a high risk of loss.
        <ul>
            <li><b>Typical Duration</b>: Days to months</li>
            <div class="duration-bar" style="width: 20%;"></div>
            <li><b>Expected Return</b>: Very high, but with very high risk</li>
            <div class="return-bar" style="width: 90%;"></div>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="custom-box">
        <h2>3. Cryptocurrencies</h2>
        <p>
        Cryptocurrencies are highly volatile digital assets that can offer substantial returns over short periods.
        They are suitable for investors who can tolerate extreme price swings.
        <ul>
            <li><b>Typical Duration</b>: Days to months</li>
            <div class="duration-bar" style="width: 20%;"></div>
            <li><b>Expected Return</b>: Very high, but with very high risk</li>
            <div class="return-bar" style="width: 90%;"></div>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="custom-box">
        <h2>4. Individual Stocks</h2>
        <p>
        Investing in individual stocks can offer high returns in a short period, but also comes with higher risk.
        Short-term trading can be very volatile.
        <ul>
            <li><b>Typical Duration</b>: Less than 1 year</li>
            <div class="duration-bar" style="width: 15%;"></div>
            <li><b>Expected Return</b>: High, but with significant risk</li>
            <div class="return-bar" style="width: 80%;"></div>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# 返回按钮
if st.button("Back to Assessment"):
    st.switch_page("pages/7_risktolerance.py")

