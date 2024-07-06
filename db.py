import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Numeric
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

# User credential model
class Credential(Base):
    __tablename__ = 'credentials'
    userid = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), unique=True, nullable=False)

# User information model
class User(Base):
    __tablename__ = 'userinfo'
    userid = Column(Integer, unique=True, primary_key=True)
    birthday = Column(Date, nullable=False)
    country = Column(String(255), nullable=False)
    currency = Column(String(10), nullable=False)
    savings = Column(Numeric(10, 2), nullable=True)

# Plan information model
class Plan(Base):
    __tablename__ = 'plans'
    planid = Column(Integer, unique=True, primary_key=True)
    userid = Column(Integer)
    goal_age = Column(Integer)
    goal_duration = Column(Integer)
    payment_duration = Column(Integer)
    total_amount = Column(Numeric(10, 2), nullable=True)
    payment_first = Column(Numeric(10, 2), nullable=True)
    payment_last = Column(Numeric(10, 2), nullable=True)
    payment_monthly = Column(Numeric(10, 2), nullable=True)

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
