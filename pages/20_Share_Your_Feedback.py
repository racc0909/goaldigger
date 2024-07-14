import streamlit as st
from db import showChosenPages, logout

showChosenPages()

logout()

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 加载 CSS 文件
css_file_path = "data/titlestyle.css"
load_css(css_file_path)

def feedback_page():
    st.markdown(
        f"""
        <h1>We Value Your Feedback</h1>
        """,
        unsafe_allow_html=True
    )
    st.markdown("""
    Your feedback is important to us! Please take a moment to share your thoughts and suggestions about our web app.
    """)

    st.subheader("How would you rate your overall experience?")
    overall_experience = st.slider("Rate from 1 to 5", 1, 5)

    st.subheader("What do you like about our web app?")
    likes = st.text_area("Enter your positive feedback here")

    st.subheader("What can we improve?")
    improvements = st.text_area("Enter your suggestions for improvement here")

    st.subheader("Additional comments or suggestions")
    additional_comments = st.text_area("Enter any additional comments here")

    if st.button("Submit Feedback"):
        # Simulating feedback submission process
        st.success("Thank you for your feedback! We appreciate your input.")
        # Here you would typically save the feedback to a database or send it to an email

if __name__ == "__main__":
    feedback_page()
