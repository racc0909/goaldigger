import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import hashlib

# Database setup
DATABASE_URL = "postgresql+psycopg2://username:password@host/database"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

Base.metadata.create_all(engine)

# Helper functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    user = session.query(User).filter_by(username=username).first()
    if user and user.password == hash_password(password):
        return user
    return None

def signup(username, password):
    if session.query(User).filter_by(username=username).first():
        return False
    user = User(username=username, password=hash_password(password))
    session.add(user)
    session.commit()
    return True

# Streamlit app
def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = authenticate(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.user_id = user.id
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password")

def signup_page():
    st.title("Sign Up")
    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")
    if st.button("Sign Up"):
        if signup(username, password):
            st.success("User created successfully!")
        else:
            st.error("Username already taken")

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if st.session_state.logged_in:
        st.sidebar.title("Navigation")
        st.sidebar.write("Go to 'Form' or 'Overview' from the sidebar.")
    else:
        auth_choice = st.sidebar.selectbox("Login or Sign Up", ["Login", "Sign Up"])
        if auth_choice == "Login":
            login_page()
        elif auth_choice == "Sign Up":
            signup_page()

if __name__ == "__main__":
    main()
