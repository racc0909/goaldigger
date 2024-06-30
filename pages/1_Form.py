import streamlit as st
from db import session, FormData

def form_page():
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        st.title("Form Page")
        data = st.text_input("Enter some data")
        if st.button("Submit"):
            new_data = FormData(user_id=st.session_state.user_id, data=data)
            session.add(new_data)
            session.commit()
            st.success("Data submitted")
    else:
        st.warning("Please log in to access this page.")
        st.stop()

if __name__ == "__main__":
    form_page()
