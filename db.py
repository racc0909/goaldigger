import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, date
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
    user_id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), unique=True, nullable=False)

# User information model
class Userinfo(Base):
    __tablename__ = 'userinfo'
    user_id = Column(Integer, unique=True, primary_key=True)
    user_nickname = Column(String(255), nullable=False)
    user_birthday = Column(Date, nullable=False)
    user_country = Column(String(255), nullable=False)
    user_currency = Column(String(10), nullable=False)

# Plan information model
class Plan(Base):
    __tablename__ = 'plans'
    plan_id = Column(Integer, unique=True, primary_key=True)
    user_id = Column(Integer)
    created_on = Column(Date, nullable=False)
    goal_type = Column(String(255), nullable=False)
    goal_name = Column(String(255), nullable=False)
    goal_age = Column(Integer)
    goal_date = Column(Date, nullable=False)
    goal_total = Column(Numeric(10, 2), nullable=False)
    goal_target = Column(Numeric(10, 2), nullable=False)
    goal_target_monthly = Column(Numeric(10, 2), nullable=False)
    saving_initial = Column(Numeric(10, 2), nullable=False)
    saving_duration = Column(Integer)
    saving_interest = Column(Numeric(10, 2), nullable=False)
    payment_first_percent = Column(Numeric(10, 2), nullable=True)
    payment_first = Column(Numeric(10, 2), nullable=True)
    payment_last_percent = Column(Numeric(10, 2), nullable=True)
    payment_last = Column(Numeric(10, 2), nullable=True)
    loan_duration = Column(Integer)
    loan_startdate = Column(Date)
    loan_amount = Column(Numeric(10, 2))
    loan_interest = Column(Numeric(10, 2))
    loan_monthly = Column(Numeric(10, 2))

# Saving information model
class Saving(Base):
    __tablename__ = 'savings'
    user_id = Column(Integer)
    plan_id = Column(Integer)
    saving_id = Column(Integer, unique=True, primary_key=True)
    saving_date = Column(Date, primary_key=True)
    saving_amount = Column(Numeric(10, 2), primary_key=True)

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
        st.switch_page("Goaldigger.py")
        st.experimental_rerun()

def backToOverview():
    # Button to backToOverview
      if st.sidebar.button("Back to Overview"):
        #del st.session_state.edit_plan_id
        st.switch_page("Goaldigger.py")

### --- USER INFO ---
def getUserInfo(user_id):
    info = session.query(Userinfo).filter_by(user_id=user_id).first()
    return info

def createOrUpdateUserInfo(user_id, user_nickname, user_country, user_currency, user_birthday):
    info = getUserInfo(user_id)
    if info:
        info.user_nickname = user_nickname
        info.user_country = user_country
        info.user_currency = user_currency
        info.user_birthday = user_birthday
    else:
        info = Userinfo(
            user_id=user_id, user_nickname=user_nickname, user_country=user_country, user_currency=user_currency, user_birthday=user_birthday
        )
        session.add(info)
    session.commit()
    return info

# Calculate date function
def calculateGoalDate(user_birthday, goal_age):
    """
    Calculate the goal date by adding goal_age years to the user's birthday.
    """
    # Calculate the goal date
    goal_date = user_birthday + timedelta(days=goal_age * 365.25)  # Approximately accounts for leap years
    return goal_date

def calculateSavingDuration(goal_date):
    """
    Calculate the number of days from today until the goal date.
    """
    today = datetime.today()
    # Calculate the duration in days
    duration_days = (goal_date - today).days
    return duration_days

def calculateGoalAge(user_birthday, goal_date):
    """
    Calculate the goal age by substracting goal_date to the user's birthday and get the lower number
    """
    # Calculate the difference in years
    goal_age = goal_date.year - user_birthday.year
    
    # Adjust for cases where the goal date is before the birthday in the year
    if (goal_date.month, goal_date.day) < (user_birthday.month, user_birthday.day):
        goal_age -= 1
    
    return goal_age

def calculateUserAge(user_birthday):
    """
    Calculate the user age by substracting today to the user's birthday and get the lower number
    """
    # Calculate the difference in years
    today = date.today()
    user_age = today.year - user_birthday.year
    
    # Adjust for cases where the goal date is before the birthday in the year
    if (today.month, today.day) < (user_birthday.month, user_birthday.day):
        user_age -= 1
    
    return user_age


### --- PLANS ---
def createPlan(user_id, goal_type, goal_name, goal_age, goal_date, 
                goal_total, goal_target, goal_target_monthly, 
                saving_initial, saving_interest, saving_duration,
                payment_first_percent, payment_first, payment_last_percent, payment_last, 
                loan_duration, loan_startdate, loan_amount, loan_interest, loan_monthly):

    # Add plan to to the SQL table
    plan = Plan(
                user_id=user_id, 
                goal_type=goal_type, 
                goal_name=goal_name, 
                goal_age=goal_age, 
                goal_date=goal_date, 
                goal_total=goal_total, 
                goal_target=goal_target, 
                goal_target_monthly=goal_target_monthly,
                saving_initial=saving_initial, 
                saving_interest=saving_interest, 
                saving_duration=saving_duration,
                payment_first_percent=payment_first_percent, 
                payment_first=payment_first, 
                payment_last_percent=payment_last_percent, 
                payment_last=payment_last, 
                loan_duration=loan_duration, 
                loan_startdate=loan_startdate, 
                loan_amount=loan_amount, 
                loan_interest=loan_interest, 
                loan_monthly=loan_monthly
                )
    session.add(plan)
    session.commit()
    return True

def getUserPlans(user_id):
    return session.query(Plan).filter_by(user_id=user_id).all()

def getPlan(plan_id):
    return session.query(Plan).filter_by(plan_id=plan_id).first()

def updatePlan(plan_id, goal_name, goal_age, goal_date, 
                goal_total, goal_target, goal_target_monthly, 
                saving_initial, saving_interest, saving_duration,
                payment_first_percent, payment_first, payment_last_percent, payment_last, 
                loan_duration, loan_startdate, loan_amount, loan_interest, loan_monthly):
    plan = getPlan(plan_id)
    if plan:
        plan.plan_id = plan_id,
        plan.goal_name=goal_name, 
        plan.goal_age=goal_age, 
        plan.goal_date=goal_date, 
        plan.goal_total=goal_total, 
        plan.goal_target=goal_target, 
        plan.goal_target_monthly=goal_target_monthly,
        plan.saving_initial=saving_initial, 
        plan.saving_interest=saving_interest, 
        plan.saving_duration=saving_duration,
        plan.payment_first_percent=payment_first_percent, 
        plan.payment_first=payment_first, 
        plan.payment_last_percent=payment_last_percent, 
        plan.payment_last=payment_last, 
        plan.loan_duration=loan_duration, 
        plan.loan_startdate=loan_startdate, 
        plan.loan_amount=loan_amount, 
        plan.loan_interest=loan_interest, 
        plan.loan_monthly=loan_monthly
        session.commit()
        return True
    return False

def deletePlan(plan_id):
    plan = getPlan(plan_id)
    if plan:
        session.delete(plan)
        session.commit()
        return True
    return False

### --- SAVINGS ---
def createSaving(user_id, plan_id, saving_date, saving_amount):
    saving = Saving(user_id=user_id, plan_id=plan_id, saving_date=saving_date, saving_amount=saving_amount)
    session.add(saving)
    session.commit()
    return True

def getTotalSavings(user_id, plan_id):
    total_savings = session.query(Saving).filter_by(user_id=user_id, plan_id=plan_id).all()
    return sum([saving.saving_amount for saving in total_savings])

def getSavings(user_id, plan_id):
    return session.query(Saving).filter_by(user_id=user_id, plan_id=plan_id).all()