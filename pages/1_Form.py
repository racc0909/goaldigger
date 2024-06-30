import streamlit as st
from db import session, FormData

def form_page():
    st.title("Form Page")
    data = st.text_input("Enter some data")
    if st.button("Submit"):
        new_data = FormData(user_id=st.session_state.user_id, data=data)
        session.add(new_data)
        session.commit()
        st.success("Data submitted")

if __name__ == "__main__":
    form_page()