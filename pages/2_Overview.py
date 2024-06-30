import streamlit as st
from db import session, FormData

def overview_page():
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        st.title("Overview")
        user_id = st.session_state.user_id
        data_entries = session.query(FormData).filter_by(user_id=user_id).all()
        for entry in data_entries:
            st.write(f"Data ID: {entry.id} - Data: {entry.data}")
    else:
        st.warning("Please log in to access this page.")
        st.stop()

if __name__ == "__main__":
    overview_page()
