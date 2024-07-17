import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, timedelta, date
from financial_plan import display_timeline, display_piechart, filter_plans_by_date, filter_loans_by_date
from db import getUserInfo, getUserPlans, getTotalSavings, logout, createSaving
from db import authenticate, signup, logout, deletePlan, showChosenPages
import time

# Set page title and icon
st.set_page_config(page_title="Goaldigger", page_icon=":moneybag:")

showChosenPages()

# Way one
sidebar_logo = "img/Logo_Without_Text.png"
st.logo(sidebar_logo, link="https://goaldigger.streamlit.app/", icon_image="img/Logo_Without_Text.png")

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_file_path = "data/titlestyle.css"
load_css(css_file_path)

def login_page():
      # Google Fonts
      st.markdown(
         """
         <style>
         @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Montserrat+Alternates:wght@400&display=swap');

         h1 {
               font-family: 'Montserrat', sans-serif;
               color: #4535C1;
         }
         .custom-subheader {
               font-family: 'Montserrat', sans-serif;
               color: #478CCF;
               font-size: 24px;
         }
         </style>
         """,
         unsafe_allow_html=True
      )

      # Welcome page
      st.markdown(
         f"""
         <h1>✨ Welcome to Goaldigger ✨</h1>
         """,
         unsafe_allow_html=True
      )
      st.divider()
      st.write("Empowering you to reach your financial dreams, from your next big purchase to a comfortable retirement. Whether it's short-term savings or long-term investments, we're here to guide you every step of the way.")
      st.write("""
               🏆 This project represents the hard work and dedication of [Shiya Li](https://www.linkedin.com/in/shiya-li-19676620a), [Nhu Nguyen](https://www.linkedin.com/in/maithaonhunguyen), and [Linh Ha Le](https://www.linkedin.com/in/linh-ha-le), created over 4 weeks for the course "Financial Economics with Python" in the Summer Semester of 2024 🏆
               """)

      # Signup and Login Page
      if "signup_mode" not in st.session_state:
         st.session_state.signup_mode = False

      if not st.session_state.signup_mode:
         # Login
         st.markdown(
               f"""
               <h2 class="custom-subheader">Login</h2>
               """,
               unsafe_allow_html=True
         )
         username = st.text_input("Username")
         password = st.text_input("Password", type="password")
         if st.button("Login"):
               # Function to authenticate the user
               user = authenticate(username, password)
               if user:
                  st.session_state.logged_in = True
                  st.session_state.user_id = user.user_id
                  st.success("Login successfully!")
                  time.sleep(0.1)
                  st.experimental_rerun()
               else:
                  st.error("Invalid username or password.")

         st.markdown(
               """
               <p style="font-family: 'Montserrat', sans-serif; color: #7776B3; font-size: 14px;">New here?</p>
               """,
               unsafe_allow_html=True
         )
         if st.button("Create an account!"):
               st.session_state.signup_mode = True
               st.experimental_rerun()

         # Tip box content
         tip_message = """
         **💡**
         We don't require your real data for signup. But if you prefer not to register a new user, you have the option to use a pre-made login.

         Feel free check out our app with:
         - **Username:** fake_user
         - **Password:** fake_password
         """

         # Display the tip box
         st.warning(tip_message)
      else:
         # Sign up
         st.markdown(
            f"""
            <h2 class="custom-subheader">Sign Up</h2>
            """,
            unsafe_allow_html=True
         )
         username = st.text_input("New Username")
         password = st.text_input("New Password", type="password")
         if st.button("Sign Up"):
            # Function to add user to database
            if signup(username, password):
                  st.balloons()
                  st.success("User created successfully!")
                  st.session_state.signup_mode = False
                  # Automatically logging in
                  user = authenticate(username, password)
                  st.session_state.user_id = user.user_id
                  st.session_state.logged_in = True
                  time.sleep(0.5)
                  st.switch_page("pages/1_Personal_Information.py")
            else:
                  st.error("Username already taken")
         
         if st.button("Back to Login"):
            st.session_state.signup_mode = False
            st.experimental_rerun()

def main():
    # Content of the main page
    if 'logged_in' not in st.session_state:
      st.session_state.logged_in = False
    
    if st.session_state.logged_in:
      
      logout()

      # Helper function to get a list of years
      def get_years(start_year, end_year):
         return [str(year) for year in range(start_year, end_year + 1)]

      @st.experimental_dialog("📊 Add Saving Progress")
      def add_saving(user_id, plan):
         profile = getUserInfo(user_id)
         if '%%' in plan.goal_name:
            plan.goal_name, saved_selected_make, saved_selected_model = plan.goal_name.split('%%')

         st.header(f"Plan: {plan.goal_name}")
         months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
         years = get_years(datetime.now().year - 3, datetime.now().year + 7)
         col1, col2 = st.columns([2, 1])
         selected_month = col1.selectbox ("📅 Select month", months, index=datetime.now().month - 1)
         selected_year = col2.selectbox("📅 Select year", years, index=years.index(str(datetime.now().year)))

         # Map the month name to its corresponding number
         month_number = months.index(selected_month) + 1

         # Combine selected_year, month_number, and day 01 into a date
         savings_date = datetime(int(selected_year), month_number, 1)
         savings_amount = st.number_input(f"🪙 Saving Amount for {savings_date.strftime('%B %Y')} ({profile.user_currency})", value=float(plan.goal_target_monthly))

         col1_1, col1_2 = st.columns([1, 1])
         with col1_1:
            if st.button("✅ Submit"):
               st.balloons()
               createSaving(user_id, plan.plan_id, savings_date, savings_amount)
               st.success("Saving added successfully!")
               time.sleep(0.3)
               del st.session_state.add_saving_plan_id
               st.rerun()
                  
         with col1_2:
            if st.button("❌ Cancel"):
               st.info("Saving canceled.")
               time.sleep(0.3)
               del st.session_state.add_saving_plan_id
               st.rerun()


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
         # Process each plan to split the goal_name if it contains '%%'
         for plan in plans:
            if '%%' in plan.goal_name:
               plan.goal_name, _, _ = plan.goal_name.split('%%')
               
         st.markdown(
             f"""
             <h1>Overview of All Financial Plans for {profile.user_nickname}</h1>
             """,
             unsafe_allow_html=True
         )
         st.divider()
         # CSS for custom styling
         st.markdown("""
            <style>
            .plan-box {
               background-color: #f4f4f4;
               padding: 10px;
               margin: 10px;
               border-radius: 10px;
               width: 100%;
            }
            .delete-button {
               background-color: red;
               color: white;
               border: none;
               padding: 5px 10px;
               cursor: pointer;
            }
            .savings-term {
               margin-top: 5px;
            }
            #wholetext {
               border: 2px solid #ddd;
               padding: 10px;
               background-color: #f4f4f4;
               border-radius: 10px;
            }
            </style>
            """, unsafe_allow_html=True)

         # Rearrange plans
         st.markdown(
             f"""
             <h2 class="custom-subheader">Rearrange Plans</h2>
             """,
             unsafe_allow_html=True
         )
         plan_order = st.multiselect("Drag to reorder plans", options=[plan.goal_name for plan in plans], default=[plan.goal_name for plan in plans])
         #plans = [plan for name in plan_order for plan in plans if plan.goal_name == name]

         # Date selection
         selected_date = st.date_input("Select month and year to view savings distribution", date.today(), min_value=date.today(), format="DD.MM.YYYY")
         selected_date = datetime.combine(selected_date, datetime.min.time())  # Ensure selected_date is datetime

         # Filter plans based on the selected date
         filtered_plans = filter_plans_by_date(plans, selected_date)

         # Calculate savings distribution
         total_monthly_savings = sum(plan.goal_target_monthly for plan in filtered_plans)
         savings_distribution = {plan.goal_name: plan.goal_target_monthly for plan in filtered_plans}

         # Filter loans based on the selected date and calculate total monthly loans
         total_monthly_loans = filter_loans_by_date(plans, selected_date)
         if total_monthly_loans > 0:
               savings_distribution['Loans/Mortgages'] = total_monthly_loans

         # Calculate the total amount
         total_amount = total_monthly_savings + total_monthly_loans

         # Display Pie chart
         display_piechart(user_id, savings_distribution)

         # Display Timeline
         display_timeline(user_id)

         # Check if filtered_plans is not empty
         if filtered_plans:
            # Graph for total savings over time
            savings_data = {'Date': [], 'Total Savings': []}
            start_date = datetime.today()
            end_date = max(plan.goal_date if isinstance(plan.goal_date, datetime) else datetime.combine(plan.goal_date, datetime.min.time()) for plan in filtered_plans)
            current_date = start_date

            while current_date <= end_date:
               current_monthly_savings = sum(plan.goal_target_monthly for plan in filter_plans_by_date(plans, current_date))
               savings_data['Date'].append(current_date)
               savings_data['Total Savings'].append(current_monthly_savings)
               current_date += timedelta(days=30)  # Move to next month

            savings_df = pd.DataFrame(savings_data)

            # Create the figure
            fig_savings = go.Figure()
            fig_savings.add_trace(go.Scatter(
               x=savings_df['Date'], 
               y=savings_df['Total Savings'], 
               mode='lines+markers', 
               name='Total Savings',
               hovertemplate="Year: %{x|%Y}, Total savings: %{y:.2f}<extra></extra>"
            ))

            # Update layout
            fig_savings.update_layout(
               title='Total Savings Over Time',
               xaxis_title='Date',
               yaxis_title=f'Total Savings ({profile.user_currency})',
               xaxis=dict(tickmode='linear', dtick="M12", tickformat="%Y"),
               showlegend=True,
               height=300
            )
            st.plotly_chart(fig_savings)

         else:
            st.info("No plans available to display the savings graph.")

         # Show each plan
         # Plans with loans
         st.markdown(
             f"""
             <h2 class="costum-subheader">Saving Plans Summary</h2>
             """,
             unsafe_allow_html=True
         )
         for i, plan in enumerate([plan for plan in plans]): 
            if '%%' in plan.goal_name:
               plan.goal_name, saved_selected_make, saved_selected_model = plan.goal_name.split('%%')
            total_saving = getTotalSavings(user_id, plan.plan_id)
            rest_saving = plan.goal_target - total_saving  
            with st.container(border=True):
               col1_1, col1_2, col1_3 = st.columns([3, 1, 1.2])
               with col1_1:
                  st.markdown(f"<h3>📋 {plan.goal_name}</h3>", unsafe_allow_html=True)
               with col1_2:
                  if st.button(f"✏️ View plan", key=f"edit_{plan.plan_id}_{i}"):
                     st.session_state.edit_plan_id = plan.plan_id
                     st.switch_page("pages/3_Edit_Plan.py")
               with col1_3:
                  if st.button(f"🗑️ Delete plan", key=f"delete_{plan.plan_id}_{i}"):
                     deletePlan(plan.plan_id)
                     st.experimental_rerun()
                   
               # Tabs
               if plan.loan_amount > 0:
                  tab1, tab2, tab3 = st.tabs(["📊 Saving Progress", "📝 Plan Details", "💳 Loan Details"])
                  with tab3:
                     st.markdown(f"<p style='color: blue;'><strong>Monthly Loan Payment:</strong> {plan.goal_target_monthly:,.2f} {'EUR'}</p>", unsafe_allow_html=True)
                     st.markdown(f"<p><strong>Total Loan Payment:</strong> {plan.loan_amount:,.2f} {'EUR'}</p>", unsafe_allow_html=True)
                     st.markdown(f"<p><strong>Loan End Date:</strong> {plan.loan_startdate.strftime('%d.%m.%Y')} to {(plan.loan_startdate + pd.DateOffset(years=plan.loan_duration)).strftime('%d.%m.%Y')}</p>", unsafe_allow_html=True)
               
               else:
                  tab1, tab2 = st.tabs(["📊 Saving Progress", "📝 Plan Details"])

               with tab1:
                  st.markdown(f"<p style='margin: 1;'><strong>Current Savings:</strong> {total_saving:,.2f} {'EUR'}</p>", unsafe_allow_html=True)
                  st.markdown(f"<p style='margin: 1;'><strong>Rest Amount Needed:</strong> {rest_saving:,.2f} {'EUR'}</p>", unsafe_allow_html=True)

                  if plan.goal_target > 0:
                     progress = min(float(total_saving / plan.goal_target), 1.0)
                     st.progress(progress)

                  else:
                     st.warning("Target amount for this plan is zero, cannot show graph.")

                  if rest_saving <= 0:
                     st.balloons()

               with tab2:
                  st.markdown(f"<p><strong>Target Amount:</strong> {plan.goal_target:,.2f} {'EUR'}</p>", unsafe_allow_html=True)
                  st.markdown(f"<p><strong>Due Date:</strong> {plan.goal_date.strftime('%d.%m.%Y')}</p>", unsafe_allow_html=True)
                  st.markdown(f"<p style='margin: 1;'><strong>Monthly Savings Needed:</strong> {plan.goal_target_monthly:,.2f} {'EUR'}</p>", unsafe_allow_html=True)
                  
               st.markdown("</div>", unsafe_allow_html=True)

               # BUTTONS
               col1_1, col1_2 = st.columns([2, 1])
               with col1_1:
                  if st.button(f"📈 Grow your savings", key=f"invest_{plan.plan_id}_{i}"):
                     st.session_state.invest_plan_id = plan.plan_id
                     st.switch_page("pages/7_Risk_Tolerance_Assessment.py")
               with col1_2:
                  if st.button(f"✅ Add Saving", key=f"add_saving_{plan.plan_id}_{i}"):
                     st.session_state.add_saving_plan_id = plan.plan_id
                     add_saving(user_id, plan)

    else:
         login_page()

if __name__ == "__main__":
    main()
