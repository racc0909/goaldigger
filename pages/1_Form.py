import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database setup
DATABASE_URL = "mysql+mysqlconnector://username:password@localhost/streamlit_app"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Form data model
class FormData(Base):
    __tablename__ = 'form_data'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    data = Column(String(255))

Base.metadata.create_all(engine)

def form_page():
    st.title("Form Page")
    data = st.text_input("Enter some data")
    if st.button("Submit"):
        new_data = FormData(user_id=st.session_state.user_id, data=data)
        session.add(new_data)
        session.commit()
        st.success("Data submitted")

if 'logged_in' in st.session_state and st.session_state.logged_in:
    form_page()
else:
    st.write("Please log in to access this page.")
