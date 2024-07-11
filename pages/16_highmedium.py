#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st

# 页面标题
st.title("Recommended Investment Options for High Risk and Medium Term")

# 描述
st.write("Based on your high risk tolerance and preference for medium-term investments, we recommend the following options:")

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
        <h2>1. Individual Stocks</h2>
        <p>
        Investing in individual stocks can offer high returns, but also comes with higher risk.
        Diversifying your stock portfolio can help manage risk.
        <ul>
            <li><b>Typical Duration</b>: 3 to 5 years</li>
            <div class="duration-bar" style="width: 60%;"></div>
            <li><b>Expected Return</b>: High, but with significant risk</li>
            <div class="return-bar" style="width: 80%;"></div>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="custom-box">
        <h2>2. Real Estate Investment Trusts (REITs)</h2>
        <p>
        REITs allow you to invest in real estate without directly owning property.
        They often provide high dividends and have the potential for appreciation.
        <ul>
            <li><b>Typical Duration</b>: 3 to 7 years</li>
            <div class="duration-bar" style="width: 60%;"></div>
            <li><b>Expected Return</b>: Moderate to high, with moderate risk</li>
            <div class="return-bar" style="width: 60%;"></div>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="custom-box">
        <h2>3. High-Yield Corporate Bonds (Junk Bonds)</h2>
        <p>
        High-yield corporate bonds, also known as junk bonds, offer higher returns than investment-grade bonds but come with higher risk.
        They are issued by companies with lower credit ratings.
        <ul>
            <li><b>Typical Duration</b>: 2 to 5 years</li>
            <div class="duration-bar" style="width: 60%;"></div>
            <li><b>Expected Return</b>: High, but with higher risk</li>
            <div class="return-bar" style="width: 75%;"></div>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="custom-box">
        <h2>4. Mutual Funds/ETFs with Aggressive Growth</h2>
        <p>
        Mutual funds and ETFs that focus on aggressive growth invest in companies with high growth potential.
        These funds are diversified but can be volatile.
        <ul>
            <li><b>Typical Duration</b>: 3 to 5 years</li>
            <div class="duration-bar" style="width: 60%;"></div>
            <li><b>Expected Return</b>: High, but with higher volatility</li>
            <div class="return-bar" style="width: 80%;"></div>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# 返回按钮
if st.button("Back to Assessment"):
    st.switch_page("pages/7_risktolerance.py")
if st.button("I want to compare opotions"):
    st.switch_page("pages/18_options_comparison.py")
