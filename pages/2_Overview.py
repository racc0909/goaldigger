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

def overview_page():
    st.title("Overview")
    user_id = st.session_state.user_id
    data_entries = session.query(FormData).filter_by(user_id=user_id).all()
    for entry in data_entries:
        st.write(f"Data ID: {entry.id} - Data: {entry.data}")

if 'logged_in' in st.session_state and st.session_state.logged_in:
    overview_page()
else:
    st.write("Please log in to access this page.")
