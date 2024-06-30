import streamlit as st
from db import authenticate, signup

def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = authenticate(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.user_id = user.id
            st.success("Logged in successfully!")
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

def signup_page():
    st.title("Sign Up")
    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")
    if st.button("Sign Up"):
        if signup(username, password):
            st.success("User created successfully!")
        else:
            st.error("Username already taken")

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if st.session_state.logged_in:
        page = st.sidebar.selectbox("Select a page", ["Form", "Overview"])
        if page == "Form":
            st.experimental_set_page("pages/form_page.py")
        elif page == "Overview":
            st.experimental_set_page("pages/overview_page.py")
    else:
        auth_choice = st.sidebar.selectbox("Login or Sign Up", ["Login", "Sign Up"])
        if auth_choice == "Login":
            login_page()
        elif auth_choice == "Sign Up":
            signup_page()

if __name__ == "__main__":
    main()
