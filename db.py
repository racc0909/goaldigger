import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import hashlib

# Read database credentials from Streamlit secrets
db_config = st.secrets["postgresql"]
DATABASE_URL = f"postgresql+psycopg2://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

# Database setup
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
    birthday = Column(Date, nullable=False)
    country = Column(String(100), nullable=False)
    currency = Column(String(10), nullable=False)

# Form data model
class FormData(Base):
    __tablename__ = 'form_data'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    data = Column(String(255))

Base.metadata.create_all(engine)

# Helper functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    user = session.query(User).filter_by(username=username).first()
    if user and user.password == hash_password(password):
        return user
    return None

def signup(username, password, birthday, country, currency):
    if session.query(User).filter_by(username=username).first():
        return False
    birthday = birthday.strftime("%Y-%m-%d")
    user = User(username=username, password=hash_password(password), birthday=birthday, country=country, currency=currency)
    session.add(user)
    session.commit()
    return True
