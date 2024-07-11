#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st

# 页面标题
st.title("Recommended Investment Options for Medium Risk and Long Term")

# 描述
st.write("Based on your medium risk tolerance and preference for long-term investments, we recommend the following options:")

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
        <h2>1. Diversified Stock Portfolios</h2>
        <p>
        Investing in a diversified portfolio of stocks can offer substantial returns over the long term.
        Diversification helps manage risk while aiming for growth.
        <ul>
            <li><b>Typical Duration</b>: 5 to 10 years or more</li>
            <div class="duration-bar" style="width: 90%;"></div>
            <li><b>Expected Return</b>: Moderate to high, with moderate risk</li>
            <div class="return-bar" style="width: 60%;"></div>
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
            <li><b>Typical Duration</b>: 5 to 10 years</li>
            <div class="duration-bar" style="width: 90%;"></div>
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
        <h2>3. Balanced Mutual Funds</h2>
        <p>
        Balanced mutual funds invest in a mix of stocks and bonds, aiming to balance risk and return.
        They provide moderate returns and are less volatile than pure equity funds.
        <ul>
            <li><b>Typical Duration</b>: 5 to 10 years</li>
            <div class="duration-bar" style="width: 90%;"></div>
            <li><b>Expected Return</b>: Moderate, with a balanced risk profile</li>
            <div class="return-bar" style="width: 50%;"></div>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="custom-box">
        <h2>4. Corporate Bonds (Investment-Grade)</h2>
        <p>
        Investment-grade corporate bonds are issued by financially stable companies and offer higher returns than government bonds.
        They are suitable for long-term investments with moderate risk.
        <ul>
            <li><b>Typical Duration</b>: 5 to 10 years</li>
            <div class="duration-bar" style="width: 90%;"></div>
            <li><b>Expected Return</b>: Moderate, with relatively low risk compared to lower-grade corporate bonds</li>
            <div class="return-bar" style="width: 50%;"></div>
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
