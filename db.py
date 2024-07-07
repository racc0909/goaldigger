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
class Userinfo(Base):
    __tablename__ = 'userinfo'
    userid = Column(Integer, unique=True, primary_key=True)
    usernickname = Column(String(255), nullable=False)
    birthday = Column(Date, nullable=False)
    country = Column(String(255), nullable=False)
    currency = Column(String(10), nullable=False)
    savings = Column(Numeric(10, 2), nullable=True)

# Plan information model
class Plan(Base):
    __tablename__ = 'plans2'
    planid = Column(Integer, unique=True, primary_key=True)
    userid = Column(Integer)
    goal_title = Column(String(255), nullable=False)
    goal_age = Column(Integer)
    goal_duration = Column(Integer)
    total_amount = Column(Numeric(10, 2), nullable=True)
    payment_duration = Column(Integer)
    payment_first = Column(Numeric(10, 2), nullable=True)
    payment_last = Column(Numeric(10, 2), nullable=True)
    payment_monthly = Column(Numeric(10, 2), nullable=True)

# Saving information model
class Saving(Base):
    __tablename__ = 'savings'
    userid = Column(Integer)
    planid = Column(Integer, primary_key=True)
    savings_date = Column(Date, primary_key=True)
    savings_amount = Column(Numeric(10, 2), primary_key=True)

Base.metadata.create_all(engine)

# Helper functions
### --- SIGN UP / LOG IN / LOG OUT ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    user = session.query(Credential).filter_by(username=username).first()
    if user and user.password == hash_password(password):
        return user
    return None

def signup(username, password):
    if session.query(Credential).filter_by(username=username).first():
        return False
    # Add user credential to Credential
    credential = Credential(username=username, password=hash_password(password))
    session.add(credential)
    session.commit()
    return True

def logout():
    # Button to logout
      if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.switch_page("Goaldiggers.py")
        st.experimental_rerun()

### --- USER INFO ---
def getUserInfo(userid):
    info = session.query(Userinfo).filter_by(userid=userid).first()
    return info

def createOrUpdateUserInfo(userid, usernickname, country, currency, birthday, savings):
    info = getUserInfo(userid)
    if info:
        info.usernickname = usernickname
        info.country = country
        info.currency = currency
        info.birthday = birthday
        info.savings = savings
    else:
        info = Userinfo(
            userid=userid, usernickname=usernickname, country=country, currency=currency, birthday=birthday, savings=savings
        )
        session.add(info)
    session.commit()
    return info

### --- PLANS ---
def createPlan(userid, goal_title, goal_age, goal_duration, total_amount, payment_duration, payment_first, payment_last, payment_monthly):
    # Add plan to to the SQL table
    plan = Plan(userid=userid, goal_title=goal_title, goal_age=goal_age, goal_duration=goal_duration, 
                total_amount=total_amount, payment_duration=payment_duration, 
                payment_first=payment_first, payment_last=payment_last, payment_monthly=payment_monthly)
    session.add(plan)
    session.commit()
    return True

def getUserPlans(userid):
    return session.query(Plan).filter_by(userid=userid).all()

def getPlan(planid):
    return session.query(Plan).filter_by(planid=planid).first()

def updatePlan(planid, goal_title, goal_age, goal_duration, total_amount, payment_duration, payment_first, payment_last, payment_monthly):
    plan = getPlan(planid)
    if plan:
        plan.goal_title = goal_title
        plan.goal_age = goal_age
        plan.goal_duration = goal_duration
        plan.total_amount = total_amount
        plan.payment_duration = payment_duration
        plan.payment_first = payment_first
        plan.payment_last = payment_last
        plan.payment_monthly = payment_monthly
        session.commit()
        return True
    return False

def deletePlan(planid):
    plan = getPlan(planid)
    if plan:
        session.delete(plan)
        session.commit()
        return True
    return False

### --- SAVINGS ---
def createSaving(userid, planid, savings_date, savings_amount):
    saving = Saving(userid=userid, planid=planid, savings_date=savings_date, savings_amount=savings_amount)
    session.add(saving)
    session.commit()
    return True

def getTotalSavings(userid, planid):
    total_savings = session.query(Saving).filter_by(userid=userid, planid=planid).all()
    return sum([saving.savings_amount for saving in total_savings])