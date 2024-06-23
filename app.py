import streamlit as st
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher
import pandas as pd
import pickle
import time
from pathlib import Path
from datetime import datetime, timedelta

#import psycopg2

# Page title
st.set_page_config(page_title='Financial Goal Planer', page_icon='🎫')

# --- USER AUTHENTICATION ---
names = ["Peter Parker", "Rebecca Miller"]
usernames = ["pparker", "rmiller"]

# Load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pk1"
# rb (read) and load instead of wb (write) and dump
with file_path.open("rb") as file:
  hashed_passwords = pickle.load(file)

credentials = {"usernames":{}}
        
for uname,name,pwd in zip(usernames,names,hashed_passwords):
    user_dict = {"name": name, "password": pwd}
    credentials["usernames"].update({uname: user_dict})
    
# Create authentication object
# Calculator is for cookie, abdef is a random str
authenticator = stauth.Authenticate(credentials, "cookie_name", "random_key", cookie_expiry_days = 0)

name, authentication_status, username = authenticator.login('main', fields = {'Form name': 'Login'})

if authentication_status == False:
   st.error("Username/password is incorrect")
   st.session_state.authentication_status = False

if authentication_status == None:
   st.warning("Please enter your username and password")
   st.session_state.authentication_status = None

if authentication_status:
   st.session_state.authentication_status = True

   st.title('🎫 Financial Goal Planer')

   # SIDEBAR
   st.sidebar.title(f"Welcome {name}")
   st.sidebar.success("Select a demo above.")
   authenticator.logout("Logout", "sidebar")

   # Creat data if not exists
   if 'df_userinfo' not in st.session_state:
      df_userinfo = pd.DataFrame(columns=['ID', 'username', 'regular_income', 'additional_income', 'regular_expenses', 'additional_expenses', 'debt_expenses', 'savings', 'investments', 'Status', 'date'])
      st.session_state.df_userinfo = df_userinfo

   # CREATING A PLAN
   with st.form('Current situation'):
      st.header('Income')
      st.info('To help you get a clear picture of your financial situation, we\'d love for you to answer a few questions. If you\'re unsure about some information, just enter your best estimate — you can always change it later!')
      regular_income = st.number_input("What is your current regular income after taxes?", 0, 1000000)  
      additional_income = st.number_input("What is your income from other sources after taxes?", 0, 1000000)
      # todo: Raises
      st.header('Expenses')    
      regular_expenses = st.number_input("What are your monthly regular expenses?", 0, 1000000)     
      additional_expenses = st.number_input("How much do you set aside for additional monthly expenses?", 0, 1000000)  
      debt_expenses = st.number_input("What are your monthly debt obligations (e.g., loan payments, credit card payments)?", 0, 1000000)  
      st.header('Savings and Investments')    
      savings = st.number_input("How much do you save each month?", 0, 1000000)   
      investments = st.number_input("How much do you invest each month?", 0, 1000000) 
      submit = st.form_submit_button('Save')

      if submit:
         today_date = datetime.now().strftime('%m-%d-%Y_%H-%M-%S')
         df = pd.DataFrame([{'ID': f'INFO-{username}-{today_date}',
                              'username': username,                              
                              'regular_income': regular_income,
                              'additional_income': additional_income,
                              'regular_expenses': regular_expenses,
                              'additional_expenses': additional_expenses,
                              'debt_expenses': debt_expenses,
                              'savings': savings,
                              'investments': investments,
                              'Status': 'Open',
                              'date': today_date
                           }])
         st.success('Information saved!')
         time.sleep(0.5)
         st.session_state.df_userinfo = pd.concat([st.session_state.df_userinfo, df], axis=0).sort_values(by=['ID'], ascending=[False])
         st.switch_page("pages/1_Overview.py")


