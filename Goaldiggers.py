import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from db import authenticate, signup, logout
import time

# Way one
# st.logo("data/Goal_Digger-removebg-preview (1)", link="data/Goal_Digger-removebg-preview (1).png", icon_image=None)
# 定义图片路径
sidebar_logo = "data/Goal_Digger-removebg-preview (1).png"
st.logo(sidebar_logo)

# Logo on the Sidebar
st.sidebar.logo("data/Goal_Digger-removebg-preview (1)", icon_image=None)

# Set page title and icon
st.set_page_config(page_title="Goaldiggers", page_icon=":moneybag:")
# Function to display the logout button

def login_page():
   # todo: Introduction to the app
   st.title("Welcome to Goaldiggers")
   st.write("Helping you achieve your financial goals, both short-term and long-term.")

   # Signup and Login Page
   if "signup_mode" not in st.session_state:
        st.session_state.signup_mode = False

   if not st.session_state.signup_mode:
      # Login
      st.subheader("Login")
      username = st.text_input("Username")
      password = st.text_input("Password", type="password")
      if st.button("Login"):
         # Function to authenticate the user
         user = authenticate(username, password)
         if user:
            st.session_state.logged_in = True
            st.session_state.user_id = user.user_id
            st.success("Login successfully!")
            time.sleep(0.8)
            st.experimental_rerun()
         else:
            st.error("Invalid username or password.")
      st.write("Don't have an account?")
      if st.button("Go to Sign Up"):
         st.session_state.signup_mode = True
         st.experimental_rerun()
   else:
      # Sign up
      st.subheader("Sign Up")
      username = st.text_input("New Username")
      password = st.text_input("New Password", type="password")

      if st.button("Sign Up"):
         # Function to add user to database
         if signup(username, password):
            st.success("User created successfully!")
            st.session_state.signup_mode = False
            # Automatically logging in
            user = authenticate(username, password)
            st.session_state.user_id = user.user_id
            st.session_state.logged_in = True
            time.sleep(0.5)
            #st.experimental_rerun()
            st.switch_page("pages/1_User_Info.py")
         else:
            st.error("Username already taken")

def main():
    # Content of the main page
    if 'logged_in' not in st.session_state:
      st.session_state.logged_in = False
    
    if st.session_state.logged_in:
      
      logout()

      # First page
      st.title("Investment Options Comparison Calculator")
      st.write("Enter your investment amount and term to simulate the expected returns on different investment options.")

      # 利率信息
      cd_rates = {
         '1_year': 0.0434,  # 4.34%
         '3_year': 0.03,    # 假设为3.0%
         '5_year': 0.035    # 假设为3.5%
      }

      gov_bond_rates = {
         '1_year': 0.015,  # 1.5%
         '3_year': 0.02,   # 2.0%
         '5_year': 0.025   # 2.5%
      }

      money_market_rates = {
         '1_year': 0.0065,  # 0.65%
         '3_year': 0.01,    # 假设为1.0%
         '5_year': 0.015    # 假设为1.5%
      }

      investment_amount = st.number_input("Investment Amount (€)", min_value=0, value=125000)
      investment_term = st.selectbox("Investment Term (Years)", [1, 3, 5])

      def calculate_return(amount, years, rate):
         return amount * (1 + rate) ** years

      if st.button("Calculate"):
         term_str = f'{investment_term}_year'
         cd_return = calculate_return(investment_amount, investment_term, cd_rates[term_str])
         gov_bond_return = calculate_return(investment_amount, investment_term, gov_bond_rates[term_str])
         money_market_return = calculate_return(investment_amount, investment_term, money_market_rates[term_str])
      
         st.write(f"Expected return after {investment_term} years:")
         st.write(f"Certificate of Deposit (CD): {cd_return:.2f} €")
         st.write(f"Government Bonds: {gov_bond_return:.2f} €")
         st.write(f"Money Market Funds: {money_market_return:.2f} €")
      
         # 图表展示
         terms = [1, 3, 5]
         cd_returns = [calculate_return(investment_amount, term, cd_rates[f'{term}_year']) for term in terms]
         gov_bond_returns = [calculate_return(investment_amount, term, gov_bond_rates[f'{term}_year']) for term in terms]
         money_market_returns = [calculate_return(investment_amount, term, money_market_rates[f'{term}_year']) for term in terms]

         plt.figure(figsize=(10, 6))
         plt.plot(terms, cd_returns, marker='o', label='Certificate of Deposit (CD)')
         plt.plot(terms, gov_bond_returns, marker='o', label='Government Bonds')
         plt.plot(terms, money_market_returns, marker='o', label='Money Market Funds')
         plt.title("Investment Returns Over Different Terms")
         plt.xlabel("Investment Term (Years)")
         plt.ylabel("Expected Return (€)")
         plt.legend()
         plt.grid(True)
         st.pyplot(plt)

    else:
         login_page()

if __name__ == "__main__":
    main()
