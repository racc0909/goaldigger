import streamlit as st
from db import getUserInfo, createOrUpdateUserInfo, logout, showChosenPages
from datetime import datetime
import time

showChosenPages()

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
            st.markdown(
                f"""
                <h2 class="custom-subheader">Your Profile</h2>
                """,
                unsafe_allow_html=True
            )
            user_nickname = st.text_input("Your Name", profile.user_nickname)
            user_birthday = st.date_input("Your Birthday", profile.user_birthday, format="DD.MM.YYYY")
            user_country = st.selectbox("Your Country", list(country_data.keys()), index=list(country_data.keys()).index(profile.user_country) if profile.user_country else 0)
            user_currency = st.selectbox("Currency", country_data[user_country]['Currency'], index=0)
            user_subscription = st.selectbox("Choose subscription:", ("Standard", "Premium"), index=0 if profile.user_subscription == "Standard" else 1)
            mode = "edit"
        else:
            st.markdown(
                f"""
                <h2 class="custom-subheader">Create Your Profile</h2>
                """,
                unsafe_allow_html=True
            )
            user_nickname = st.text_input("How should we call you?")
            user_birthday = st.date_input("When is your birthday?", format="DD.MM.YYYY")
            user_country = st.selectbox("Which country are you in?", list(country_data.keys()))
            user_currency = st.selectbox("Which currency are you using?", country_data[user_country]['Currency'])
            user_subscription = st.selectbox("Choose subscription:", ("Standard", "Premium"), index=0)
            mode = "create"

        if st.button("Save"):
            createOrUpdateUserInfo(user_id, user_nickname, user_country, user_currency, user_birthday, user_subscription)
            st.success("Profile saved successfully!")
            st.balloons()
            time.sleep(0.5)
            if mode == "create":
                st.switch_page("Goaldigger.py")

    else:
        st.warning("Please log in to access this page.")
        st.stop()

if __name__ == "__main__":
    user_info_page()
