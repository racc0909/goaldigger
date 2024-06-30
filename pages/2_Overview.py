import streamlit as st
from db import session, FormData

def overview_page():
    st.title("Overview")
    user_id = st.session_state.user_id
    data_entries = session.query(FormData).filter_by(user_id=user_id).all()
    for entry in data_entries:
        st.write(f"Data ID: {entry.id} - Data: {entry.data}")

if __name__ == "__main__":
    overview_page()
