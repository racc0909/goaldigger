import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta, date
from financial_plan import display_timeline
from db import getUserInfo, getUserPlans, getTotalSavings, getSavings, logout
from db import authenticate, signup, logout
import time

# Way one
sidebar_logo = "img/Logo_Without_Text.png"
st.logo(sidebar_logo, link="https://fiepdemoapp.streamlit.app/", icon_image="img/Logo_Without_Text.png")

# Logo on the Sidebar
#st.sidebar.logo("img/Logo_Without_Text.png", icon_image="img/Logo_Without_Text.png", link="https://fiepdemoapp.streamlit.app/")

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
            time.sleep(0.5)
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
            st.switch_page("pages/1_Personal_Information.py")
         else:
            st.error("Username already taken")

def main():
    # Content of the main page
    if 'logged_in' not in st.session_state:
      st.session_state.logged_in = False
    
    if st.session_state.logged_in:
      
      logout()

      # --- PERSONAL INFORMATION ---
      # PREPARATION
      # Get user info
      user_id = st.session_state.user_id
      profile = getUserInfo(user_id)
      plans = getUserPlans(user_id)

      # ---- OVERVIEW ---
      if not plans:
         st.info("No financial plans found. Please add a plan first.")
         if st.button("Add Plan"):
               st.switch_page("pages/2_Create_Plan.py")

      else:
         st.title(f"Overview of All Financial Plans for {profile.user_nickname}")

         for plan in plans:
               #savings = getSavings(user_id, plan.plan_id)
               savings_distribution = {plan.goal_name: plan.goal_target_monthly for plan in plans}

         # Rearrange plans
         st.subheader("Rearrange Plans")
         plan_order = st.multiselect("Drag to reorder plans", options=[plan.goal_name for plan in plans], default=[plan.goal_name for plan in plans])
         plans = [plan for name in plan_order for plan in plans if plan.goal_name == name]

         col1, col2 = st.columns([2, 1])

         with col1:

               # Plotting the timeline of financial goals
               display_timeline(user_id)
      
               # Pie chart for savings distribution
               fig_pie = px.pie(values=list(savings_distribution.values()), names=list(savings_distribution.keys()), title='Monthly Savings Distribution')
               st.plotly_chart(fig_pie)

         col1, col2 = st.columns(2)
         for i, plan in enumerate(plans):
               with col1 if i % 2 == 0 else col2:
                  st.markdown(f"""
                  <div style="background-color:#f4f4f4; padding: 10px; margin: 10px; border-radius: 10px;">
                     <h3>{plan.goal_name}</h3>
                     <p><strong>Target Amount:</strong> {plan.goal_target:,.2f} {profile.user_currency}</p>
                     <p><strong>Due Date:</strong> {plan.goal_date.strftime('%d.%m.%Y')}</p>
                     <p style="color: red;"><strong>Monthly Savings Needed:</strong> {plan.goal_target_monthly:,.2f} {profile.user_currency}</p>
                     <p><strong>Savings Term:</strong> {plan.saving_duration} months</p>
                  </div>
                  """, unsafe_allow_html=True)

                  # <a href="?page={plan['details_link']}">{plan['details_link']}</a>
                  # todo: delete, edit, add saving
                  # <form action="?delete_plan={i}" method="post">
                  #     <button type="submit" style="background-color: red; color: white; border: none; padding: 5px 10px; cursor: pointer;">🗑️ Delete</button>
                  # </form>

    else:
         login_page()

if __name__ == "__main__":
    main()
