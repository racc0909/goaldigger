import streamlit as st
from sqlalchemy import create_engine, extract, func, Column, Integer, String, Date, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta, date
import hashlib
from st_pages import Page, show_pages, hide_pages

# Read database credentials from Streamlit secrets
db_config = st.secrets["postgresql"]
DATABASE_URL = f"postgresql+psycopg2://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

# Database setup
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
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
    user_subscription = Column(String(255), nullable=False)

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
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    session = Session()
    try:
        user = session.query(Credential).filter_by(username=username).first()
        if user and user.password == hash_password(password):
            return user
        return None
    except SQLAlchemyError as e:
        session.rollback()
        print(f"An error occurred: {e}")
        return None
    finally:
        session.close()

def signup(username, password):
    session = Session()
    try:
        if session.query(Credential).filter_by(username=username).first():
            return False
        # Add user credential to Credential
        credential = Credential(username=username, password=hash_password(password))
        session.add(credential)
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"An error occurred: {e}")
        return False
    finally:
        session.close()

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
    session = Session()
    try:
        info = session.query(Userinfo).filter_by(user_id=user_id).first()
        return info
    except SQLAlchemyError as e:
        session.rollback()
        print(f"An error occurred: {e}")
        return None
    finally:
        session.close()

def createOrUpdateUserInfo(user_id, user_nickname, user_country, user_currency, user_birthday, user_subscription):
    session = Session()
    try:
        info = session.query(Userinfo).filter_by(user_id=user_id).first()
        if info:
            info.user_nickname = user_nickname
            info.user_country = user_country
            info.user_currency = user_currency
            info.user_birthday = user_birthday
            info.user_subscription = user_subscription
        else:
            info = Userinfo(
                user_id=user_id, user_nickname=user_nickname, user_country=user_country, user_currency=user_currency, user_birthday=user_birthday, user_subscription=user_subscription
            )
            session.add(info)
        session.commit()
        return info
    except SQLAlchemyError as e:
        session.rollback()
        print(f"An error occurred: {e}")
        return None
    finally:
        session.close()

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
    Calculate the goal age by subtracting goal_date from the user's birthday and get the lower number
    """
    # Calculate the difference in years
    goal_age = goal_date.year - user_birthday.year
    
    # Adjust for cases where the goal date is before the birthday in the year
    if (goal_date.month, goal_date.day) < (user_birthday.month, user_birthday.day):
        goal_age -= 1
    
    return goal_age

def calculateUserAge(user_birthday):
    """
    Calculate the user age by subtracting today from the user's birthday and get the lower number
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
    session = Session()
    try:
        # Add plan to the SQL table
        plan = Plan(
                    user_id=user_id, 
                    created_on=datetime.now(),
                    goal_type=goal_type, 
                    goal_name=goal_name, 
                    goal_age=goal_age, 
                    goal_date=goal_date, 
                    goal_total=round(goal_total, 2), 
                    goal_target=round(goal_target, 2), 
                    goal_target_monthly=round(goal_target_monthly, 2),
                    saving_initial=round(saving_initial, 2), 
                    saving_interest=round(saving_interest, 2), 
                    saving_duration=saving_duration,
                    payment_first_percent=round(payment_first_percent, 2), 
                    payment_first=round(payment_first, 2), 
                    payment_last_percent=round(payment_last_percent, 2), 
                    payment_last=round(payment_last, 2), 
                    loan_duration=loan_duration, 
                    loan_startdate=loan_startdate, 
                    loan_amount=round(loan_amount, 2), 
                    loan_interest=round(loan_interest, 2), 
                    loan_monthly=round(loan_monthly, 2)
                    )
        session.add(plan)
        session.commit()
        return plan.plan_id
    except SQLAlchemyError as e:
        session.rollback()
        print(f"An error occurred: {e}")
        return None
    finally:
        session.close()

def getUserPlans(user_id):
    session = Session()
    try:
        plans = session.query(Plan).filter_by(user_id=user_id).all()
        return plans
    except SQLAlchemyError as e:
        session.rollback()
        print(f"An error occurred: {e}")
        return []
    finally:
        session.close()

def getPlan(plan_id):
    session = Session()
    try:
        plan = session.query(Plan).filter_by(plan_id=plan_id).first()
        return plan
    except SQLAlchemyError as e:
        session.rollback()
        print(f"An error occurred: {e}")
        return None
    finally:
        session.close()

def updatePlan(plan_id, goal_name, goal_age, goal_date, 
                goal_total, goal_target, goal_target_monthly, 
                saving_initial, saving_interest, saving_duration,
                payment_first_percent, payment_first, payment_last_percent, payment_last, 
                loan_duration, loan_startdate, loan_amount, loan_interest, loan_monthly):
    session = Session()
    try:
        plan = session.query(Plan).filter_by(plan_id=plan_id).first()
        if plan:
            plan.goal_name = goal_name
            plan.goal_age = goal_age
            plan.goal_date = goal_date
            plan.goal_total = round(goal_total, 2)
            plan.goal_target = round(goal_target, 2)
            plan.goal_target_monthly = round(goal_target_monthly, 2)
            plan.saving_initial = round(saving_initial, 2)
            plan.saving_interest = round(saving_interest, 2)
            plan.saving_duration = saving_duration
            plan.payment_first_percent = round(payment_first_percent, 2)
            plan.payment_first = round(payment_first, 2)
            plan.payment_last_percent = round(payment_last_percent, 2)
            plan.payment_last = round(payment_last, 2)
            plan.loan_duration = loan_duration
            plan.loan_startdate = loan_startdate
            plan.loan_amount = round(loan_amount, 2)
            plan.loan_interest = round(loan_interest, 2)
            plan.loan_monthly = round(loan_monthly, 2)
            session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        session.rollback()
        print(f"An error occurred: {e}")
        return False
    finally:
        session.close()

def deletePlan(plan_id):
    session = Session()
    try:
        plan = session.query(Plan).filter_by(plan_id=plan_id).first()
        if plan:
            session.delete(plan)
            session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        session.rollback()
        print(f"An error occurred: {e}")
        return False
    finally:
        session.close()

### --- SAVINGS ---
def createSaving(user_id, plan_id, saving_date, saving_amount):
    session = Session()
    try:
        saving = Saving(user_id=user_id, plan_id=plan_id, saving_date=saving_date, saving_amount=saving_amount)
        session.add(saving)
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"An error occurred: {e}")
        return False
    finally:
        session.close()

def getSavings(user_id, plan_id):
    session = Session()
    try:
        savings = session.query(Saving).filter_by(user_id=user_id, plan_id=plan_id).all()
        return savings
    except SQLAlchemyError as e:
        session.rollback()
        print(f"An error occurred: {e}")
        return []
    finally:
        session.close()

def getTotalSavings(user_id, plan_id):
    session = Session()
    try:
        total_savings = session.query(Saving).filter_by(user_id=user_id, plan_id=plan_id).all()
        return sum([saving.saving_amount for saving in total_savings])
    except SQLAlchemyError as e:
        session.rollback()
        print(f"An error occurred: {e}")
        return 0
    finally:
        session.close()

def getTotalSavingsByYear(plan_id):
    session = Session()
    try:
        # Query the total savings by year
        total_savings_by_year = (
            session.query(extract('year', Saving.saving_date).label('year'), 
                        func.sum(Saving.saving_amount).label('total_saving'))
            .filter(Saving.plan_id == plan_id)
            .group_by(extract('year', Saving.saving_date))
            .order_by('year')
            .all()
        )

        # Convert the result to a dictionary
        savings_by_year = {int(row.year): float(row.total_saving) for row in total_savings_by_year}

        return savings_by_year
    except SQLAlchemyError as e:
        session.rollback()
        print(f"An error occurred: {e}")
        return {}
    finally:
        session.close()

def showChosenPages():
    show_pages(
        [
            Page("Goaldigger.py", "Overview", "🏠"),
            Page("pages/1_Personal_Information.py", "Personal Information", "📝"),
            Page("pages/2_Create_Plan.py", "Create Plan", "✨"),
            Page("pages/5_Investment_Options_Comparison_Calculator.py", "Bank Term Deposit Profit Calculator", ":chart_with_upwards_trend:"),
            Page("pages/7_Risk_Tolerance_Assessment.py", "Risk Tolerance Assessment", ":moneybag:"),
            Page("pages/18_options_comparison.py", "Investment Option Comparison", ":question:"),
            Page("pages/3_Edit_Plan.py", "Edit Plan"),
            Page("pages/9_Low Risk, Short Term Investments.py", "Low Risk, Short Term Investments"),
            Page("pages/10_Low Risk, Medium Term Investments.py", "Low Risk, Medium Term Investments"),
            Page("pages/11_Low Risk, Long Term Investments.py", "Low Risk, Long Term Investments"),
            Page("pages/12_Medium Risk, Short Term Investments.py", "Medium Risk, Short Term Investments"),
            Page("pages/13_Medium Risk, Medium Term Investments.py", "Medium Risk, Medium Term Investments"),
            Page("pages/14_Medium Risk, Long Term Investments.py", "Medium Risk, Long Term Investments"),
            Page("pages/15_High Risk, Short Term Investments.py", "High Risk, Short Term Investments"),
            Page("pages/16_High Risk, Medium Term Investments.py", "High Risk, Medium Term Investments"),
            Page("pages/17_High Risk, Long Term Investments.py", "High Risk, Long Term Investments"),
            Page("pages/19_includesavingprogress.py", "Tracking"),
            Page("pages/20_Share_Your_Feedback.py", "Share Your Feedback", "😃")
        ]
    )

    hide_pages(["Low Risk, Short Term Investments", "Low Risk, Medium Term Investments", "Low Risk, Long Term Investments", "Low Risk, Short Term Investments", "Medium Risk, Medium Term Investments", "Medium Risk, Long Term Investments", "Medium Risk, Short Term Investments", "High Risk, Medium Term Investments", "High Risk, Long Term Investments", "High Risk, Short Term Investments", "Edit Plan"])

