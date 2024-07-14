import streamlit as st
from db import showChosenPages, logout, createFeedback, backToOverview

showChosenPages()

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 加载 CSS 文件
css_file_path = "data/titlestyle.css"
load_css(css_file_path)

def feedback_page():
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        user_id = st.session_state.user_id
        logout()
        backToOverview()
        st.markdown(
            f"""
            <h1>We Value Your Feedback</h1>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            f"""
            <h2 class="custom-subheader">Your feedback is important to us! Please take a moment to share your thoughts and suggestions about our web app.</h2>
            """,
            unsafe_allow_html=True
        )

        st.subheader("How would you rate your overall experience?")
        overall_experience = st.slider("Rate from 1 to 5", 1, 5)

        st.subheader("What do you like about our web app?")
        likes = st.text_area("Enter your positive feedback here")

        st.subheader("What can we improve?")
        improvements = st.text_area("Enter your suggestions for improvement here")

        st.subheader("Additional comments or suggestions")
        additional_comments = st.text_area("Enter any additional comments here")

        if st.button("Submit Feedback"):
            createFeedback(user_id, overall_experience, likes, improvements, additional_comments)
            # Simulating feedback submission process
            st.success("Thank you for your feedback! We appreciate your input.")
            st.balloons()

    else:
        st.warning("Please log in to access this page.")
        st.stop()

if __name__ == "__main__":
    feedback_page()
