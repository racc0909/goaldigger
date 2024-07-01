#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import base64
from datetime import datetime, timedelta


# In[ ]:


# Function to load a local image and convert it to a base64 string
def get_image_as_base64(image_path):
    with open(image_path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")
    
# Path to the local icon
icon_path = "/Users/lishiya/Downloads/goal_digger_web_app/icons8-anzahlung-48.png"
icon_base64 = get_image_as_base64(icon_path)


# In[ ]:


def display_other_investments_page():
    st.markdown(f"""
    # Other Investment Options <img src="data:image/png;base64,{icon_base64}" width="48" style="vertical-align: middle;">
    """, unsafe_allow_html=True)
    st.markdown("""
    If you're looking for higher risk and potentially higher returns, consider the following investment options:
    """)
    st.markdown("""
    <div class="custom-box">
        <h2>Exchange-Traded Funds (ETFs)</h2>
        <p>ETFs are investment funds traded on stock exchanges, much like stocks. They hold assets such as stocks, commodities, or bonds and generally operate with an arbitrage mechanism designed to keep trading close to its net asset value, though deviations can occasionally occur.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="custom-box">
        <h2>Stocks</h2>
        <p>Investing in stocks means buying shares of ownership in a public company. Stocks have the potential for high returns, but they also come with higher risk compared to bonds and other fixed-income investments.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="custom-box">
        <h2>Commodities</h2>
        <p>Commodities are basic goods used in commerce that are interchangeable with other goods of the same type. Common commodities include gold, oil, and agricultural products. Investing in commodities can be done directly or through commodity-focused funds.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Back to Investment Suggestions", key="back_button_other"):
        del st.session_state["investment_option"]
        st.experimental_rerun()
    
if "investment_option" in st.session_state:
    option = st.session_state["investment_option"]
        
    def display_cd_page():
        st.markdown(f"""
        # Certificate of Deposit (CD) <img src="data:image/png;base64,{icon_base64}" width="48" style="vertical-align: middle;">
        """, unsafe_allow_html=True)
        st.markdown("""
        A Certificate of Deposit (CD) is a low-risk savings product offered by banks and credit unions. It offers a fixed
        interest rate for a specified term, making it a predictable and secure investment option.
        """)
        st.markdown("""
        <style>
        .custom-box {
            background-color: #f0f0f0;
            border-radius: 20px;
            padding: 10px 20px;
            margin: 10px 0;
            display: inline-block;
            width: auto;
        }
        .custom-button {
            color: white !important;  /* Change text color to white */
            background-color: #023047;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-align: center;
            display: inline-block;
            font-size: 16px;
            text-decoration: none;
            margin: 10px 0;
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="custom-box">
            <h2>Risk Assessment</h2>
            <p><strong>Risk level</strong>: Low</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="custom-box">
            <h2>Expected Returns</h2>
            <p><strong>Historical Return Rate</strong>: Typically ranges from 2% to 3.5% annually.</p>
            <p><strong>Projected Return Rate</strong>: Given the current economic conditions, expected returns are between 2.5% and 3.5% for CDs
            with terms ranging from 1 to 5 years.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="custom-box">
            <h2>Investment Term</h2>
            <p><strong>Recommended Term</strong>: Short to Medium</p>
            <ul>
                <li>Short-term Bonds: 1 to 3 years</li>
                <li>Medium-term Bonds: 3 to 10 years</li>
                <li>Long-term Bonds: 10 years or more</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Back to Investment Suggestions", key="back_button"):
            del st.session_state["investment_option"]
            st.experimental_rerun()

    def display_gov_bonds_page():
        st.markdown(f"""
        # Government Bonds <img src="data:image/png;base64,{icon_base64}" width="48" style="vertical-align: middle;">
        """, unsafe_allow_html=True)
        st.markdown("""
        Government bonds are debt securities issued by a government to support government spending and obligations.
        """)
        st.markdown("""
        <style>
        .custom-box {
            background-color: #f0f0f0;
            border-radius: 20px;
            padding: 10px 20px;
            margin: 10px 0;
            display: inline-block;
            width: auto;
        }
        .custom-button {
            color: white !important;  /* Change text color to white */
            background-color: #023047;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-align: center;
            display: inline-block;
            font-size: 16px;
            text-decoration: none;
            margin: 10px 0;
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="custom-box">
            <h2>Risk Assessment</h2>
            <p><strong>Risk level</strong>: Low</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="custom-box">
            <h2>Expected Returns</h2>
            <p><strong>Historical Return Rate</strong>: Typically ranges from 1.5% to 2.5% annually.</p>
            <p><strong>Projected Return Rate</strong>: Given the current economic conditions, expected returns are between 1.5% and 2.5% for government bonds with terms ranging from 1 to 5 years.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="custom-box">
            <h2>Investment Term</h2>
            <p><strong>Recommended Term</strong>: Medium to Long</p>
            <ul>
                <li>Short-term Bonds: 1 to 3 years</li>
                <li>Medium-term Bonds: 3 to 10 years</li>
                <li>Long-term Bonds: 10 years or more</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <a href="investment_option" class="custom-button">Back to Investment Suggestions</a>
        """, unsafe_allow_html=True)

    def display_money_market_funds_page():
        st.markdown(f"""
        # Money Market Funds <img src="data:image/png;base64,{icon_base64}" width="48" style="vertical-align: middle;">
        """, unsafe_allow_html=True)
        st.markdown("""
        Money Market Funds are mutual funds that invest in short-term, high-quality securities issued by government and corporate entities.
        """)
        st.markdown("""
        <style>
        .custom-box {
            background-color: #f0f0f0;
            border-radius: 20px;
            padding: 10px 20px;
            margin: 10px 0;
            display: inline-block;
            width: auto;
        }
        .custom-button {
            color: white !important;  /* Change text color to white */
            background-color: #023047;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-align: center;
            display: inline-block;
            font-size: 16px;
            text-decoration: none;
            margin: 10px 0;
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="custom-box">
            <h2>Risk Assessment</h2>
            <p><strong>Risk level</strong>: Low</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="custom-box">
            <h2>Expected Returns</h2>
            <p><strong>Historical Return Rate</strong>: Typically ranges from 0.5% to 1.5% annually.</p>
            <p><strong>Projected Return Rate</strong>: Given the current economic conditions, expected returns are between 0.5% and 1.5% for money market funds.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="custom-box">
            <h2>Investment Term</h2>
            <p><strong>Recommended Term</strong>: Very Short</p>
            Money market funds can be used for short-term investments and are highly liquid, making them suitable for funds that need to be accessible on short notice.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <a href="javascript:window.history.back();" class="custom-button">Back to Investment Suggestions</a>
        """, unsafe_allow_html=True)
            
            
    if option == "Certificate of Deposit (CD)":
            display_cd_page()
    elif option == "Government Bonds":
            display_gov_bonds_page()
    elif option == "Money Market Funds":
        display_money_market_funds_page()

else:
    st.title("Plan Your Investments")
    st.write("We provide low-risk investment options to help you preserve or grow your savings while you work towards your goals.")
    investment_options = {
        "Certificate of Deposit (CD)": "Low risk, interest rate around 2%-3%",
        "Government Bonds": "Low risk, interest rate around 3%-4%",
        "Money Market Funds": "Low risk, interest rate around 1.5%-2.5%"
    }

    # 使用图标
    with open("/Users/lishiya/Downloads/goal_digger_web_app/icons8-anzahlung-48.png", "rb") as file:
        cd_icon = file.read()
    gov_bond_icon_url = "https://www.flaticon.com/svg/static/icons/svg/1170/1170638.svg"
    money_market_icon_url = "https://www.flaticon.com/svg/static/icons/svg/1170/1170674.svg"

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(cd_icon, width=50)
        st.subheader("Certificate of Deposit (CD)")
        st.write(investment_options["Certificate of Deposit (CD)"])
        if st.button("Learn more", key="cd"):
            st.session_state["investment_option"] = "Certificate of Deposit (CD)"

    with col2:
        st.image(gov_bond_icon_url, width=50)
        st.subheader("Government Bonds")
        st.write(investment_options["Government Bonds"])
        if st.button("Learn more", key="gov_bond"):
            st.session_state["investment_option"] = "Government Bonds"

    with col3:
        st.image(money_market_icon_url, width=50)
        st.subheader("Money Market Funds")
        st.write(investment_options["Money Market Funds"])
        if st.button("Learn more", key="money_market"):
            st.session_state["investment_option"] = "Money Market Funds"
        
    # 在底部增加点击链接
    st.markdown("""
    <div style="margin-top: 20px;">
        <a href="#" onclick="window.location.href='/#Other Investment Options';">Not satisfied with low-risk options? Discover other possible investments</a>
    </div>
    """, unsafe_allow_html=True)

