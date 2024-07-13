import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, timedelta, date
from financial_plan import display_timeline, display_piechart, filter_plans_by_date
from db import getUserInfo, getUserPlans, getTotalSavings, logout
from db import authenticate, signup, logout, deletePlan
import time

# Way one
sidebar_logo = "img/Logo_Without_Text.png"
st.logo(sidebar_logo, link="https://fiepdemoapp.streamlit.app/", icon_image="img/Logo_Without_Text.png")

# Set page title and icon
st.set_page_config(page_title="Goaldigger", page_icon=":moneybag:")

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_file_path = "data/titlestyle.css"
load_css(css_file_path)

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
        .custom-subheader {
            font-family: 'Montserrat', sans-serif;
            color: #478CCF;
            font-size: 24px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 使用 HTML 和 CSS 更改标题颜色和字体
    st.markdown(
        f"""
        <h1>✨ Welcome to Goaldigger ✨</h1>
        """,
        unsafe_allow_html=True
    )
    st.divider()
    st.write("Empowering you to reach your financial dreams, from your next big purchase to a comfortable retirement. Whether it's short-term savings or long-term investments, we're here to guide you every step of the way.")

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
        st.write("Don't have an account?")
        if st.button("Go to Sign Up"):
            st.session_state.signup_mode = True
            st.experimental_rerun()
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
         plans = [plan for name in plan_order for plan in plans if plan.goal_name == name]

         # Date selection
         selected_date = st.date_input("Select month and year to view savings distribution", date.today(), min_value=date.today(), format="DD.MM.YYYY")

         # Filter plans based on the selected date
         filtered_plans = []
         for plan in plans:
            due_date = plan.goal_date.date() if isinstance(plan.goal_date, datetime) else plan.goal_date
            if due_date >= selected_date:
                filtered_plans.append(plan)
         
         for plan in filtered_plans:
               total_monthly_savings = sum(plan.goal_target_monthly for plan in filtered_plans)
               total_monthly_loans = sum(plan.loan_monthly for plan in filtered_plans)
               total_amount = total_monthly_savings + total_monthly_loans

               savings_distribution = {plan.goal_name: plan.goal_target_monthly for plan in filtered_plans}
               # Adding loan/mortgage amounts to savings distribution
               if total_monthly_loans > 0:
                  savings_distribution['Loans/Mortgages'] = total_monthly_loans

         # Display Pie chart
         display_piechart(user_id, savings_distribution)

         # Display Timeline
         display_timeline(user_id)

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

         # Show each plan
         # Plans with loans
         st.subheader(" Saving Plans Summary")
         col1, col2 = st.columns(2)
         for i, plan in enumerate([plan for plan in plans if plan.goal_target_monthly]): 
            total_saving = getTotalSavings(user_id, plan.plan_id)
            rest_saving = plan.goal_target - total_saving     
            with col1 if i % 2 == 0 else col2:
               st.markdown(
                  f"""
                  <div id="wholetext" style="background-color:#f4f4f4; padding: 10px; margin: 10px; border-radius: 10px;">
                        <div class="plan-box">
                           <h3>{plan.goal_name}</h3>
                           <p><strong>Target Amount:</strong> {plan.goal_target:,.2f} {profile.user_currency}</p>
                           <p><strong>Due Date:</strong> {plan.goal_date.strftime('%d.%m.%Y')}</p>
                           <p style="margin: 1;"><strong>Monthly Savings Needed:</strong> {plan.goal_target_monthly:,.2f} {profile.user_currency}</p>
                           <p style="margin: 1; color: red;"><strong>Current Savings:</strong> {total_saving:,.2f} {profile.user_currency}</p>
                           <p style="margin: 1; color: red;"><strong>Rest Amount Needed:</strong> {rest_saving:,.2f} {profile.user_currency}</p>
                           <div style='background-color:#e0f7fa; padding: 10px; border-radius: 10px;'>
                              <p style='color: blue;'><strong>Monthly Savings needed for Loan Payment:</strong> {plan.goal_target_monthly:,.2f} {profile.user_currency}</p>
                              <p><strong>Total Loan Payment:</strong> {plan.loan_amount:,.2f} {profile.user_currency}</p>
                              <p><strong>Loan End Date:</strong> {plan.loan_startdate.strftime('%d.%m.%Y')} to {(plan.loan_startdate + pd.DateOffset(years=plan.loan_duration)).strftime('%d.%m.%Y')}</p>
                           </div>
                        </div>
                  </div>
                  """, unsafe_allow_html=True
               )
            
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

         # Plans without loans
         st.subheader("")
         col1, col2 = st.columns(2)
         for i, plan in enumerate([plan for plan in plans if plan.goal_target_monthly == False]):
            total_saving = getTotalSavings(user_id, plan.plan_id)
            rest_saving = plan.goal_target - total_saving     
            with col1 if i % 2 == 0 else col2:
               st.markdown(
                  f"""
                  <div id="wholetext" style="background-color:#f4f4f4; padding: 10px; margin: 10px; border-radius: 10px;">
                        <div class="plan-box">
                           <h3>{plan.goal_name}</h3>
                           <p><strong>Target Amount:</strong> {plan.goal_target:,.2f} {profile.user_currency}</p>
                           <p><strong>Due Date:</strong> {plan.goal_date.strftime('%d.%m.%Y')}</p>
                           <p style="margin: 1;"><strong>Monthly Savings Needed:</strong> {plan.goal_target_monthly:,.2f} {profile.user_currency}</p>
                           <p style="margin: 1; color: red;"><strong>Current Savings:</strong> {total_saving:,.2f} {profile.user_currency}</p>
                           <p style="margin: 1; color: red;"><strong>Rest Amount Needed:</strong> {rest_saving:,.2f} {profile.user_currency}</p>
                        </div>
                  </div>
                  """, unsafe_allow_html=True
               )
            
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
