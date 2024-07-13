import streamlit as st
from datetime import datetime
from db import getPlan, createSaving, logout
import time

def add_saving_page():
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        logout()
        user_id = st.session_state.user_id

        if 'add_saving_plan_id' in st.session_state:
            add_saving_plan_id = st.session_state.add_saving_plan_id
            plan = getPlan(add_saving_plan_id)  # Retrieve the plan details
            st.subheader(f"Add Saving to {plan.goal_name}")
            savings_date = st.date_input("Saving's date", value=datetime.today(), format="DD.MM.YYYY")
            savings_amount = st.number_input("Amount", value=float(plan.goal_target_monthly))

            if st.button("Save Saving"):
                createSaving(user_id, add_saving_plan_id, savings_date, savings_amount)
                st.success("Saving added successfully!")
                time.sleep(0.8)
                del st.session_state.add_saving_plan_id
                st.switch_page("Goaldigger.py")

            if st.button("Cancel"):
                st.info("Saving canceled.")
                time.sleep(0.5)
                del st.session_state.add_saving_plan_id
                st.switch_page("Goaldigger.py")

    else:
        st.warning("Please log in to access this page.")
        st.stop()

if __name__ == "__main__":
    add_saving_page()