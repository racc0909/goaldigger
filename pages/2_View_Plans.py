import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from db import getUserPlans, updatePlan, deletePlan, getPlan, logout, createSaving, getTotalSavings

def view_plans_page():
    st.title("Your Plans")

    if 'logged_in' in st.session_state and st.session_state.logged_in:
        # Logout button
        logout()

        # Page content
        user_id = st.session_state.user_id
        plans = getUserPlans(user_id)

        if not plans:
            st.info("You have no plans.")
            return

        for plan in plans:
            total_saving = getTotalSavings(user_id, plan.plan_id)

            col1, col2 = st.columns([3, 1])
            with col1:
                with st.expander(f"{plan.goal_name} (Goal Age: {plan.goal_age})"):
                    st.write(f"Duration: {plan.saving_duration} years")
                    st.write(f"Total Amount: ${plan.goal_total}")
                    st.write(f"Total Savings: ${total_saving}")

                    col1_1, col1_2, col1_3 = st.columns([3, 0.8, 0.8])
                    with col1_1:
                        if st.button("✅ Add Saving", key=f"add_saving_{plan.plan_id}"):
                            st.session_state.add_saving_plan_id = plan.plan_id
                            st.experimental_rerun()
                    with col1_2:
                        if st.button("✏️ Edit", key=f"edit_{plan.plan_id}"):
                            st.session_state.edit_plan_id = plan.plan_id
                            st.experimental_rerun()
                    with col1_3:
                        if st.button("🗑️ Delete", key=f"delete_{plan.plan_id}"):
                            deletePlan(plan.plan_id)
                            st.experimental_rerun()

            with col2:
                # Plotting the graph
                fig, ax = plt.subplots()
                categories = ['Total Amount', 'Total Savings']
                values = [plan.goal_total, total_saving]
                ax.barh(categories, values, color=['blue', 'green'], alpha=0.7)
                ax.set_xlabel('Amount')
                ax.set_title('Total Savings vs Total Amount')
                st.pyplot(fig)

        # if 'edit_plan_id' in st.session_state:
        #     edit_plan_id = st.session_state.edit_plan_id
        #     plan = getPlan(edit_plan_id)
        #     if plan:
        #         st.subheader("Edit Plan")
        #         goal_name = st.text_input("Goal Title", value=plan.goal_name)
        #         goal_age = st.number_input("Goal Age", value=plan.goal_age)
        #         saving_duration = st.number_input("Goal Duration (years)", value=plan.saving_duration)
        #         goal_total = st.number_input("Total Amount", value=plan.goal_total)
        #         payment_duration = st.number_input("Payment Duration (months)", value=plan.payment_duration)
        #         payment_first = st.number_input("First Payment", value=plan.payment_first)
        #         payment_last = st.number_input("Last Payment", value=plan.payment_last)
        #         payment_monthly = st.number_input("Monthly Payment", value=plan.payment_monthly)

        #         if st.button("Save Changes"):
        #             updatePlan(edit_plan_id, goal_name, goal_age, saving_duration, goal_total, payment_duration, payment_first, payment_last, payment_monthly)
        #             st.success("Plan updated successfully!")
        #             del st.session_state.edit_plan_id
        #             st.experimental_rerun()

        #         if st.button("Cancel"):
        #             del st.session_state.edit_plan_id
        #             st.experimental_rerun()
        
        if 'add_saving_plan_id' in st.session_state:
            add_saving_plan_id = st.session_state.add_saving_plan_id
            st.subheader("Add Saving")
            savings_date = st.date_input("Date", value=datetime.today())
            savings_amount = st.number_input("Amount", value=100.00)

            if st.button("Save Saving"):
                createSaving(user_id, add_saving_plan_id, savings_date, savings_amount)
                st.success("Saving added successfully!")
                del st.session_state.add_saving_plan_id
                st.experimental_rerun()

            if st.button("Cancel"):
                del st.session_state.add_saving_plan_id
                st.experimental_rerun()

    else:
        st.warning("Please log in to access this page.")
        st.stop()

if __name__ == "__main__":
    view_plans_page()
