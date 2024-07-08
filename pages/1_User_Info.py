import streamlit as st
from db import getUserInfo, createOrUpdateUserInfo, logout
from datetime import datetime
import pycountry

# A mapping from countries to their currencies
COUNTRY_CURRENCY_MAP = {country.name: country.alpha_3 for country in pycountry.countries}
COUNTRY_CURRENCY = {
    'United States': 'USD',
    'Canada': 'CAD',
    'United Kingdom': 'GBP',
    'Germany': 'EUR',
    'France': 'EUR',
    'Italy': 'EUR',
    'Spain': 'EUR',
    'China': 'CNY',
    'Japan': 'JPY',
    'India': 'INR',
    'Australia': 'AUD',
    'Brazil': 'BRL',
    'Viet Nam': 'VND'
    # Add more countries and currencies as needed
}

def user_info_page():
    st.title("📝 Personal Information")

    if 'logged_in' in st.session_state and st.session_state.logged_in:
        user_id = st.session_state.user_id

        # Button to logout
        logout()

        profile = getUserInfo(user_id)

        if profile:
            st.subheader("Your Profile")
            user_nickname = st.text_input("Name", profile.user_nickname)
            user_birthday = st.date_input("Birthday", profile.user_birthday, format="DD.MM.YYYY")
            user_country = st.selectbox("Country", list(COUNTRY_CURRENCY_MAP.keys()), index=list(COUNTRY_CURRENCY_MAP.keys()).index(profile.user_country) if profile.user_country else 0)
            user_currency = st.selectbox("Currency", [COUNTRY_CURRENCY.get(user_country)], index=0)
        else:
            st.subheader("Create Your Profile")
            user_nickname = st.text_input("How should we call you?")
            user_birthday = st.date_input("When is your birthday?", format="DD.MM.YYYY")
            user_country = st.selectbox("Which country are you in?", list(COUNTRY_CURRENCY_MAP.keys()))
            user_currency = st.selectbox("Which currency are you using?", [COUNTRY_CURRENCY.get(user_country, "")])

        if st.button("Save"):
            createOrUpdateUserInfo(user_id, user_nickname, user_country, user_currency, user_birthday)
            st.success("Profile saved successfully!")

    else:
        st.warning("Please log in to access this page.")
        st.stop()

if __name__ == "__main__":
    user_info_page()
