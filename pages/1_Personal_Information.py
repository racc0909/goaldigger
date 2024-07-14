import streamlit as st
from db import getUserInfo, createOrUpdateUserInfo, logout, showChosenPages
from datetime import datetime
import time
from st_pages import Page, show_pages, hide_pages

show_pages(
        [
            Page("Goaldigger.py", "Overview", "🏠"),
            Page("pages/1_Personal_Information.py", "Personal Information", "📝"),
            Page("pages/2_Create_Plan.py", "Create Plan", "✨"),
            Page("pages/5_Investment_Options_Comparison_Calculator.py", "Bank Term Deposit Profit Calculator", ":chart_with_upwards_trend:"),
            Page("pages/7_Risk_Tolerance_Assessment.py", "Risk Tolerance Assessment", ":moneybag:"),
            Page("pages/18_options_comparison.py", "Investment Option Comparison", ":question:"),
            Page("pages/3_Edit_Plan.py", "Edit Plan"),
            Page("pages/8_Add_Saving.py", "Add Saving"),
            Page("pages/9_Low Risk, Short Term Investments.py", "LowShort"),
            Page("pages/10_Low Risk, Medium Term Investments.py", "LowMedium"),
            Page("pages/11_Low Risk, Long Term Investments.py", "LowLong"),
            Page("pages/12_Medium Risk, Short Term Investments.py", "MediumShort"),
            Page("pages/13_Medium Risk, Medium Term Investments.py", "MediumMedium"),
            Page("pages/14_Medium Risk, Long Term Investments.py", "MediumLong"),
            Page("pages/15_High Risk, Short Term Investments.py", "HighShort"),
            Page("pages/16_High Risk, Medium Term Investments.py", "HighMedium"),
            Page("pages/17_High Risk, Long Term Investments.py", "HighLong")
        ]
    )

hide_pages(["LowShort", "LowMedium", "LowLong", "LowShort", "MediumMedium", "MediumLong", "MediumShort", "HighMedium", "HighLong", "HighShort", "Edit Plan", "Add Saving"])

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 加载 CSS 文件
css_file_path = "data/titlestyle.css"
load_css(css_file_path)

def user_info_page():
    st.markdown(
        f"""
        <h1>📝 Personal Information</h1>
        """,
        unsafe_allow_html=True
    )
    st.divider()
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        user_id = st.session_state.user_id

        # Button to logout
        logout()

        profile = getUserInfo(user_id)

        # Country selection
        country_data = {
            'Germany': {'Currency': '€', 'Inflation rate': 5.9, 'LifeExpectancy': 80.7},
            'United Kingdom': {'Currency': '£', 'Inflation rate': 6.8, 'LifeExpectancy': 82.1},
            'United States': {'Currency': '$', 'Inflation rate': 4.1, 'LifeExpectancy': 77.4}
        }

        if profile:
            st.subheader("Your Profile")
            user_nickname = st.text_input("Your Name", profile.user_nickname)
            user_birthday = st.date_input("Your Birthday", profile.user_birthday, format="DD.MM.YYYY")
            user_country = st.selectbox("Your Country", list(country_data.keys()), index=list(country_data.keys()).index(profile.user_country) if profile.user_country else 0)
            user_currency = st.selectbox("Currency", country_data[user_country]['Currency'], index=0)
            mode = "edit"
        else:
            st.subheader("Create Your Profile")
            user_nickname = st.text_input("How should we call you?")
            user_birthday = st.date_input("When is your birthday?", format="DD.MM.YYYY")
            user_country = st.selectbox("Which country are you in?", list(country_data.keys()))
            user_currency = st.selectbox("Which currency are you using?", country_data[user_country]['Currency'])
            mode = "create"

        if st.button("Save"):
            createOrUpdateUserInfo(user_id, user_nickname, user_country, user_currency, user_birthday)
            st.success("Profile saved successfully!")
            time.sleep(0.5)
            if mode == "create":
                st.switch_page("Goaldigger.py")

    else:
        st.warning("Please log in to access this page.")
        st.stop()

if __name__ == "__main__":
    user_info_page()
