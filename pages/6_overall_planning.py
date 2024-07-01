import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import plotly.graph_objs as go
from datetime import datetime, timedelta

def your_page():
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        # Nhus Code
        # Define color palette
        colors = ['#f7f7f7', '#f0f0f0', '#d9d9d9', '#bdbdbd', '#969696', '#737373', '#525252', '#252525', '#000000', '#636363']
        
        # Apply CSS for styling
        st.markdown(f"""
            <style>
                .stApp {{
                    background-color: {colors[0]};
                    color: {colors[9]};
                }}
                .sidebar .sidebar-content {{
                    background-color: {colors[1]};
                }}
                .css-1aumxhk {{
                    background-color: {colors[2]} !important;
                }}
                .css-1avcm0n {{
                    background-color: {colors[3]} !important;
                }}
                .css-1offfwp {{
                    background-color: {colors[4]} !important;
                }}
                .css-1fv8s86 {{
                    background-color: {colors[5]} !important;
                }}
                .css-1kfbxgm {{
                    background-color: {colors[6]} !important;
                }}
                .css-10trblm {{
                    background-color: {colors[7]} !important;
                }}
                .css-1d391kg {{
                    background-color: {colors[8]} !important;
                }}
                .css-1hs6hso {{
                    background-color: {colors[9]} !important;
                }}
                h1, h2, h3, h4, h5, h6 {{
                    color: {colors[9]};
                }}
                .css-145kmo2 {{
                    color: {colors[9]};
                }}
            </style>
        """, unsafe_allow_html=True)
        
        # Load car price data with caching
        @st.cache_data
        def load_car_data(file_path):
            try:
                df = pd.read_excel(file_path)
                return df
            except FileNotFoundError:
                st.error(f"File '{file_path}' not found. Please check the file path.")
                st.stop()
        
        # Function to filter models based on selected make
        def filter_models(df, selected_make):
            models = df[df['make'] == selected_make]['model'].unique()
            return models
        
        # Function to calculate monthly savings for house
        class HouseBuyingPlan:
            def __init__(self, house_price, down_payment_percent, mortgage_interest_rate, loan_term_years, current_age, target_age, inflation_rate, current_savings=0, current_savings_return=0):
                self.house_price = house_price
                self.down_payment_percent = down_payment_percent
                self.savings_interest_rate = current_savings_return if current_savings > 0 else 0
                self.mortgage_interest_rate = mortgage_interest_rate
                self.loan_term_years = loan_term_years
                self.current_age = current_age
                self.target_age = target_age
                self.inflation_rate = inflation_rate
                self.current_savings = current_savings
                self.savings_term_years = self.calculate_savings_term_years()
                self.down_payment = self.calculate_down_payment()
                self.monthly_saving = self.calculate_monthly_saving()
                self.monthly_mortgage_payment = self.calculate_monthly_mortgage_payment()
        
            def calculate_savings_term_years(self):
                return self.target_age - self.current_age
        
            def calculate_down_payment(self):
                return self.house_price * (self.down_payment_percent / 100)
        
            def calculate_monthly_saving(self):
                monthly_interest_rate = self.savings_interest_rate / 100 / 12
                number_of_payments = self.savings_term_years * 12
                if self.current_savings > 0:
                    current_savings_future_value = self.current_savings * ((1 + monthly_interest_rate) ** number_of_payments)
                    future_value_needed = self.down_payment - current_savings_future_value
                else:
                    future_value_needed = self.down_payment
                if future_value_needed <= 0:
                    return 0
                monthly_saving = npf.pmt(monthly_interest_rate, number_of_payments, 0, -future_value_needed)
                return monthly_saving
        
            def calculate_monthly_mortgage_payment(self):
                monthly_interest_rate = self.mortgage_interest_rate / 100 / 12
                number_of_payments = self.loan_term_years * 12
                loan_amount = self.house_price - self.down_payment
                monthly_payment = npf.pmt(monthly_interest_rate, number_of_payments, -loan_amount)
                return monthly_payment
        
            def calculate_savings_growth_timeline(self):
                savings_growth = []
                monthly_interest_rate = self.savings_interest_rate / 100 / 12
                total_months_saving = self.savings_term_years * 12
                total_months_mortgage = self.loan_term_years * 12
        
                # Calculate savings phase
                for month in range(total_months_saving):
                    if month == 0:
                        savings_growth.append(self.current_savings)
                    else:
                        savings_growth.append(savings_growth[-1] * (1 + monthly_interest_rate) + self.monthly_saving)
        
                # Calculate mortgage phase
                for month in range(total_months_mortgage):
                    savings_growth.append(savings_growth[-1] - self.monthly_mortgage_payment)
        
                return savings_growth
        
        # Function to calculate monthly savings for car
        class CarBuyingPlan:
            def __init__(self, car_price, down_payment_percent, loan_interest_rate, loan_term_years, current_age, target_age, inflation_rate, current_savings=0, current_savings_return=0):
                self.car_price = car_price
                self.down_payment_percent = down_payment_percent
                self.savings_interest_rate = current_savings_return if current_savings > 0 else 0
                self.loan_interest_rate = loan_interest_rate
                self.loan_term_years = loan_term_years
                self.current_age = current_age
                self.target_age = target_age
                self.inflation_rate = inflation_rate
                self.current_savings = current_savings
                self.savings_term_years = self.calculate_savings_term_years()
                self.down_payment = self.calculate_down_payment()
                self.monthly_saving = self.calculate_monthly_saving()
                self.monthly_loan_payment = self.calculate_monthly_loan_payment()
        
            def calculate_savings_term_years(self):
                return self.target_age - self.current_age
        
            def calculate_down_payment(self):
                return self.car_price * (self.down_payment_percent / 100)
        
            def calculate_monthly_saving(self):
                monthly_interest_rate = self.savings_interest_rate / 100 / 12
                number_of_payments = self.savings_term_years * 12
                if self.current_savings > 0:
                    current_savings_future_value = self.current_savings * ((1 + monthly_interest_rate) ** number_of_payments)
                    future_value_needed = self.down_payment - current_savings_future_value
                else:
                    future_value_needed = self.down_payment
                if future_value_needed <= 0:
                    return 0
                monthly_saving = npf.pmt(monthly_interest_rate, number_of_payments, 0, -future_value_needed)
                return monthly_saving
        
            def calculate_monthly_loan_payment(self):
                monthly_interest_rate = self.loan_interest_rate / 100 / 12
                number_of_payments = self.loan_term_years * 12
                loan_amount = self.car_price - self.down_payment
                monthly_payment = npf.pmt(monthly_interest_rate, number_of_payments, -loan_amount)
                return monthly_payment
        
            def calculate_savings_growth_timeline(self):
                savings_growth = []
                monthly_interest_rate = self.savings_interest_rate / 100 / 12
                total_months_saving = self.savings_term_years * 12
                total_months_loan = self.loan_term_years * 12
        
                # Calculate savings phase
                for month in range(total_months_saving):
                    if month == 0:
                        savings_growth.append(self.current_savings)
                    else:
                        savings_growth.append(savings_growth[-1] * (1 + monthly_interest_rate) + self.monthly_saving)
        
                # Calculate loan phase
                for month in range(total_months_loan):
                    savings_growth.append(savings_growth[-1] - self.monthly_loan_payment)
        
                return savings_growth
        
        # Function to calculate monthly savings for pension
        class PensionPlan:
            def __init__(self, retirement_age, current_age, desired_income, annual_inflation_rate, current_savings=0, current_savings_return=0):
                self.retirement_age = retirement_age
                self.current_age = current_age
                self.desired_income = desired_income
                self.annual_inflation_rate = annual_inflation_rate
                self.current_savings = current_savings
                self.savings_interest_rate = current_savings_return if current_savings > 0 else 0
                self.years_to_retirement = self.calculate_years_to_retirement()
                self.monthly_savings_needed, self.total_savings_needed = self.calculate_pension_savings()
        
            def calculate_years_to_retirement(self):
                return self.retirement_age - self.current_age
        
            def calculate_pension_savings(self):
                monthly_income_needed_inflation_adjusted = self.desired_income / (1 + self.annual_inflation_rate / 100) ** self.years_to_retirement
                monthly_savings_needed = npf.pmt(rate=self.savings_interest_rate / 12 / 100, nper=self.years_to_retirement * 12, pv=-self.current_savings, fv=-monthly_income_needed_inflation_adjusted)
                total_savings_needed = npf.fv(rate=self.savings_interest_rate / 12 / 100, nper=self.years_to_retirement * 12, pmt=-monthly_savings_needed, pv=-self.current_savings)
                return monthly_savings_needed, total_savings_needed
        
            def calculate_savings_growth_timeline(self):
                savings_growth = []
                monthly_interest_rate = self.savings_interest_rate / 100 / 12
                total_months_saving = self.years_to_retirement * 12
        
                # Calculate savings phase
                for month in range(total_months_saving):
                    if month == 0:
                        savings_growth.append(self.current_savings)
                    else:
                        savings_growth.append(savings_growth[-1] * (1 + monthly_interest_rate) + self.monthly_savings_needed)
        
                return savings_growth
        
        # Main Streamlit app
        def main():
            st.title('Financial Planning Calculator')
        
            # Navigation sidebar
            st.sidebar.title("Navigation")
            selection = st.sidebar.radio("Go to", ["Overall Plan", "Housing Plan", "Car Plan", "Pension Plan", "Actual Savings"])
        
            # Personal Information
            with st.sidebar:
                st.header('Personal Information')
                current_age = st.number_input('Enter your current age', min_value=0, max_value=100, step=1, key='current_age')
                inflation_rate = st.slider('Enter the annual inflation rate (%):', min_value=0.0, max_value=10.0, value=2.0, step=0.1, key='annual_inflation_rate')
        
            if 'house_plan' not in st.session_state:
                st.session_state.house_plan = None
            if 'car_plan' not in st.session_state:
                st.session_state.car_plan = None
            if 'pension_plan' not in st.session_state:
                st.session_state.pension_plan = None
            if 'actual_savings' not in st.session_state:
                st.session_state.actual_savings = {}
        
            if selection == "Overall Plan":
                st.header('Overall Financial Plan')
                st.subheader('Savings Growth and Timeline')
        
                if st.session_state.house_plan or st.session_state.car_plan or st.session_state.pension_plan:
                    events = []
                    savings_growth_timeline = np.zeros(1)
                    months = np.zeros(1)
        
                    if st.session_state.house_plan:
                        house_plan = st.session_state.house_plan
                        events.append(('Buy House', house_plan.target_age))
                        house_savings_growth = house_plan.calculate_savings_growth_timeline()
                        savings_growth_timeline = np.append(savings_growth_timeline, house_savings_growth)
                        months = np.append(months, np.arange(len(house_savings_growth)) / 12 + current_age)
        
                    if st.session_state.car_plan:
                        car_plan = st.session_state.car_plan
                        events.append(('Buy Car', car_plan.target_age))
                        car_savings_growth = car_plan.calculate_savings_growth_timeline()
                        savings_growth_timeline = np.append(savings_growth_timeline, car_savings_growth)
                        months = np.append(months, np.arange(len(car_savings_growth)) / 12 + current_age)
        
                    if st.session_state.pension_plan:
                        pension_plan = st.session_state.pension_plan
                        events.append(('Retire', pension_plan.retirement_age))
                        pension_savings_growth = pension_plan.calculate_savings_growth_timeline()
                        savings_growth_timeline = np.append(savings_growth_timeline, pension_savings_growth)
                        months = np.append(months, np.arange(len(pension_savings_growth)) / 12 + current_age)
        
                    events.sort(key=lambda x: x[1])
        
                    fig = go.Figure()
        
                    fig.add_trace(go.Scatter(x=months, y=savings_growth_timeline, mode='lines', name='Planned Savings Growth'))
        
                    for event in events:
                        fig.add_trace(go.Scatter(x=[event[1]], y=[savings_growth_timeline[int((event[1] - current_age) * 12)]],
                                                 mode='markers+text', text=[f'{event[0]} ({event[1]})'], textposition='top center',
                                                 name=event[0]))
        
                    # Add actual savings data
                    if st.session_state.actual_savings:
                        actual_savings_df = pd.DataFrame(list(st.session_state.actual_savings.items()), columns=["Month", "Amount"]).sort_values(by="Month")
                        actual_savings_df["Cumulative"] = actual_savings_df["Amount"].cumsum()
                        actual_months = [current_age + (datetime.strptime(date, '%Y-%m') - datetime(datetime.now().year, datetime.now().month, 1)).days / 365 for date in actual_savings_df["Month"]]
                        fig.add_trace(go.Scatter(x=actual_months, y=actual_savings_df["Cumulative"], mode='lines+markers', name='Actual Savings'))
        
                    fig.update_layout(
                        title='Savings Growth Over Time',
                        xaxis_title='Age',
                        yaxis_title='Total Savings ($)',
                        showlegend=True
                    )
        
                    st.plotly_chart(fig)
        
                    # Pie Chart
                    total_savings_needed = {
                        'House Down Payment': house_plan.down_payment if st.session_state.house_plan else 0,
                        'Car Down Payment': car_plan.down_payment if st.session_state.car_plan else 0,
                        'Pension Savings': pension_plan.total_savings_needed if st.session_state.pension_plan else 0
                    }
        
                    fig_pie = go.Figure(data=[go.Pie(labels=list(total_savings_needed.keys()), values=list(total_savings_needed.values()))])
                    fig_pie.update_layout(title='Savings Allocation')
                    st.plotly_chart(fig_pie)
                else:
                    st.write("Please enter your details for housing, car, and pension plans to see the overall financial plan.")
        
            elif selection == "Housing Plan":
                st.header('Housing Plan')
                house_price = st.number_input('Enter the house price:', min_value=0.0, format="%.2f", key='house_price')
                house_down_payment_percent = st.slider('Enter the down payment percentage:', min_value=0.0, max_value=100.0, step=0.1, format="%.1f", key='house_down_payment_percent')
                house_mortgage_interest_rate = st.slider('Enter the annual interest rate on mortgage:', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='house_mortgage_interest_rate')
                house_loan_term_years = st.number_input('Enter the loan term in years:', value=30, min_value=0, max_value=100, step=1, key='house_loan_term_years')
                house_target_age = st.number_input('Enter the age you want to acquire a house:', min_value=current_age + 1, max_value=100, step=1, key='house_target_age')
                house_current_savings = st.number_input('Enter your current savings for the house (optional):', min_value=0.0, format="%.2f", key='house_current_savings')
        
                house_current_savings_return = 0
                if house_current_savings > 0:
                    house_current_savings_return = st.slider('Enter the annual return on current savings:', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='house_current_savings_return')
        
                if st.button('Calculate House Plan'):
                    if current_age >= house_target_age:
                        st.error("Target age must be greater than current age.")
                    else:
                        st.session_state.house_plan = HouseBuyingPlan(house_price, house_down_payment_percent, house_mortgage_interest_rate, house_loan_term_years, current_age, house_target_age, inflation_rate, house_current_savings, house_current_savings_return)
        
                if st.session_state.house_plan:
                    house_plan = st.session_state.house_plan
                    st.write(f"**House Price:** ${house_plan.house_price:,.2f}")
                    st.write(f"**Down Payment ({house_plan.down_payment_percent}%):** ${house_plan.down_payment:,.2f}")
                    st.write(f"**Monthly Savings Needed for Down Payment:** ${house_plan.monthly_saving:,.2f}")
                    st.write(f"**Monthly Mortgage Payment:** ${house_plan.monthly_mortgage_payment:,.2f}")
                    st.write(f"**Savings Term:** {house_plan.savings_term_years} years")
        
            elif selection == "Car Plan":
                st.header('Car Plan')
                car_option = st.radio('Choose an Option:', ('See Available Suggested Car Prices', 'Input Your Car Price'))
        
                car_price = 0
                df = load_car_data("data/car_prices.xlsx")
        
                if car_option == 'See Available Suggested Car Prices':
                    selected_make = st.selectbox('Select Car Make', df['make'].unique(), key='selected_make')
        
                    if selected_make:
                        models = filter_models(df, selected_make)
                        selected_model = st.selectbox('Select Car Model', models, key='selected_model')
        
                        if selected_model:
                            selected_car_details = df[(df['make'] == selected_make) & (df['model'] == selected_model)]
                            car_price = float(selected_car_details['sellingprice'].values[0])
                            st.write(f"Suggested price: ${car_price:.2f}")
                            adjusted_car_price = st.number_input('Adjust the car price if needed:', min_value=0.0, value=car_price, format="%.2f", key='adjusted_car_price')
                            car_price = adjusted_car_price
        
                elif car_option == 'Input Your Car Price':
                    car_price = st.number_input('Enter the total cost of the car:', value=0.0, min_value=0.0, step=1000.0, key='car_price_input')
        
                if car_price > 0:
                    car_down_payment_percent = st.slider('Enter your down payment percentage:', min_value=0.0, max_value=100.0, step=1.0, key='car_down_payment_percent')
                    car_loan_interest_rate = st.slider('Enter the annual loan interest rate (in %):', min_value=0.0, max_value=20.0, step=0.1, key='car_loan_interest_rate')
                    car_loan_term_years = st.number_input('Enter your loan term in years:', value=5, min_value=0, max_value=100, step=1, key='car_loan_term_years')
                    car_target_age = st.number_input('Enter the age you wish to buy the car:', min_value=current_age + 1, max_value=100, step=1, key='car_target_age')
                    car_current_savings = st.number_input('Enter your current savings for the car (optional):', min_value=0.0, format="%.2f", key='car_current_savings')
        
                    car_current_savings_return = 0
                    if car_current_savings > 0:
                        car_current_savings_return = st.slider('Enter the annual return on current savings:', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='car_current_savings_return')
        
                    if st.button('Calculate Car Plan'):
                        if car_target_age <= current_age:
                            st.error("The target age must be greater than the current age.")
                        else:
                            st.session_state.car_plan = CarBuyingPlan(car_price, car_down_payment_percent, car_loan_interest_rate, car_loan_term_years, current_age, car_target_age, inflation_rate, car_current_savings, car_current_savings_return)
        
                if st.session_state.car_plan:
                    car_plan = st.session_state.car_plan
                    st.write(f"**Car Price:** ${car_plan.car_price:,.2f}")
                    st.write(f"**Down Payment ({car_plan.down_payment_percent}%):** ${car_plan.down_payment:,.2f}")
                    st.write(f"**Monthly Savings Needed for Down Payment:** ${car_plan.monthly_saving:,.2f}")
                    st.write(f"**Monthly Loan Payment:** ${car_plan.monthly_loan_payment:,.2f}")
                    st.write(f"**Savings Term:** {car_plan.savings_term_years} years")
        
            elif selection == "Pension Plan":
                st.header('Pension Plan')
                retirement_age = st.number_input('Desired retirement age', min_value=current_age + 1, max_value=100, value=65, key='retirement_age')
                current_savings = st.number_input('Current savings amount (today\'s value)', min_value=0.0, value=10000.0, key='pension_current_savings')
        
                pension_current_savings_return = 0
                if current_savings > 0:
                    pension_current_savings_return = st.slider('Enter the annual return on current savings:', min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='pension_current_savings_return')
        
                desired_income = st.number_input('Desired annual retirement income (today\'s value)', min_value=0.0, value=40000.0, key='pension_desired_income')
        
                if st.button('Calculate Pension Plan'):
                    st.session_state.pension_plan = PensionPlan(
                        retirement_age, current_age, desired_income, inflation_rate, current_savings, pension_current_savings_return
                    )
        
                if st.session_state.pension_plan:
                    pension_plan = st.session_state.pension_plan
                    st.write(f"**Monthly Savings Needed:** ${pension_plan.monthly_savings_needed:,.2f}")
                    st.write(f"**Total Savings Needed by Retirement:** ${pension_plan.total_savings_needed:,.2f}")
        
            elif selection == "Actual Savings":
                st.header("Actual Savings Tracker")
        
                # Get current year and month
                current_year = datetime.now().year
                current_month = datetime.now().month
        
                # Input for actual monthly savings
                actual_savings = st.session_state.actual_savings
                year = st.number_input("Enter year", min_value=current_year, value=current_year, step=1, key="actual_savings_year")
                month = st.number_input("Enter month", min_value=1, max_value=12, value=current_month, step=1, key="actual_savings_month")
                amount = st.number_input("Enter savings amount for this month ($):", min_value=0.0, format="%.2f", key="actual_savings_amount")
        
                if st.button("Add Savings"):
                    date_key = f"{year}-{month:02d}"
                    if date_key in actual_savings:
                        actual_savings[date_key] += amount
                    else:
                        actual_savings[date_key] = amount
                    st.session_state.actual_savings = actual_savings
                    st.success(f"Savings for {date_key} added: ${amount:.2f}")
        
                # Display actual savings
                if actual_savings:
                    st.subheader("Actual Savings History")
                    actual_savings_df = pd.DataFrame(list(actual_savings.items()), columns=["Month", "Amount"]).sort_values(by="Month")
                    st.dataframe(actual_savings_df)
        
                    # Plot actual vs planned savings
                    fig_actual_vs_planned = go.Figure()
        
                    # Combine all planned savings growth
                    combined_savings_growth = np.zeros(len(actual_savings_df))
                    if st.session_state.house_plan:
                        combined_savings_growth += np.array(st.session_state.house_plan.calculate_savings_growth_timeline()[:len(actual_savings_df)])
                    if st.session_state.car_plan:
                        combined_savings_growth += np.array(st.session_state.car_plan.calculate_savings_growth_timeline()[:len(actual_savings_df)])
                    if st.session_state.pension_plan:
                        combined_savings_growth += np.array(st.session_state.pension_plan.calculate_savings_growth_timeline()[:len(actual_savings_df)])
        
                    # Actual savings plot
                    fig_actual_vs_planned.add_trace(go.Scatter(x=actual_savings_df["Month"], y=actual_savings_df["Amount"].cumsum(), mode='lines', name='Actual Savings'))
        
                    # Planned savings plot
                    fig_actual_vs_planned.add_trace(go.Scatter(x=actual_savings_df["Month"], y=combined_savings_growth, mode='lines', name='Planned Savings'))
        
                    fig_actual_vs_planned.update_layout(
                        title='Actual vs Planned Savings',
                        xaxis_title='Month',
                        yaxis_title='Total Savings ($)',
                        showlegend=True
                    )
        
                    st.plotly_chart(fig_actual_vs_planned)
        
        if __name__ == '__main__':
            main()
        
    else:
        st.warning("Please log in to access this page.")
        st.stop()

if __name__ == "__main__":
    your_page()
