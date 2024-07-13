import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta, date
from financial_plan import display_timeline
from db import getUserInfo, getUserPlans, getTotalSavings, logout
from db import authenticate, signup, logout, deletePlan
import time

# Way one
sidebar_logo = "img/Logo_Without_Text.png"
st.logo(sidebar_logo, link="https://fiepdemoapp.streamlit.app/", icon_image="img/Logo_Without_Text.png")

# Logo on the Sidebar
#st.sidebar.logo("img/Logo_Without_Text.png", icon_image="img/Logo_Without_Text.png", link="https://fiepdemoapp.streamlit.app/")

# Set page title and icon
st.set_page_config(page_title="Goaldigger", page_icon=":moneybag:")

def login_page():
    # 引入 Google Fonts
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Montserrat+Alternates:wght@400&display=swap');

        h1 {
            font-family: 'Montserrat', sans-serif;
            color: #4535C1;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # 使用 HTML 和 CSS 更改标题颜色和字体
    st.markdown(
        f"""
        <h1>Welcome to Goaldigger</h1>
        """,
        unsafe_allow_html=True
    )

    st.write("Empowering you to reach your financial dreams, from your next big purchase to a comfortable retirement. Whether it's short-term savings or long-term investments, we're here to guide you every step of the way.")

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
            time.sleep(0.3)
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
            total_saving = getTotalSavings(user_id, plan.plan_id)
            rest_saving = plan.goal_target - total_saving
            with col1 if i % 2 == 0 else col2:
               st.markdown(f"""
               <div style="background-color:#f4f4f4; padding: 10px; margin: 10px; border-radius: 10px;">
                  <h3>{plan.goal_name}</h3>
                    <p style="margin: 1;"><strong>Target Amount:</strong> {plan.goal_target:,.2f} {profile.user_currency}</p>
                    <p style="margin: 1;"><strong>Due Date:</strong> {plan.goal_date.strftime('%d.%m.%Y')}</p>
                    <p style="margin: 1; color: red;"><strong>Current Savings:</strong> {total_saving:,.2f} {profile.user_currency}</p>
                    <p style="margin: 1; color: red;"><strong>Rest Amount Needed:</strong> {rest_saving:,.2f} {profile.user_currency}</p>
                    <p style="margin: 1;"><strong>Monthly Savings Needed:</strong> {plan.goal_target_monthly:,.2f} {profile.user_currency}</p>
                    <p style="margin: 1;"><strong>Savings Term:</strong> {plan.saving_duration} months</p>
               </div>
               """, unsafe_allow_html=True)
               
               col1_1, col1_2, col1_3 = st.columns([2, 0.8, 1])
               with col1_1:
                  if st.button(f"✅ Add Saving", key=f"add_saving_{plan.plan_id}_{i}"):
                     st.session_state.add_saving_plan_id = plan.plan_id
                     st.switch_page("pages/8_Add_Saving.py")
               with col1_2:
                  if st.button(f"✏️ Edit", key=f"edit_{plan.plan_id}_{i}"):
                     st.session_state.edit_plan_id = plan.plan_id
                     st.switch_page("pages/3_Edit_Plan.py")
               with col1_3:
                  if st.button(f"🗑️ Delete", key=f"delete_{plan.plan_id}_{i}"):
                     deletePlan(plan.plan_id)
                     st.experimental_rerun()

    else:
         login_page()

if __name__ == "__main__":
    main()
