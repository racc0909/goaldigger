import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from db import showChosenPages, logout, getUserInfo

showChosenPages()

def bank_page():
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        user_id = st.session_state.user_id
        profile = getUserInfo(user_id)
        logout()

        if profile.user_subscription == "Premium": 
            def load_css(file_path):
                with open(file_path) as f:
                    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

            # 加载 CSS 文件
            css_file_path = "data/titlestyle.css"
            load_css(css_file_path)

            # Bank data
            banks = {
                "ING Bank": {
                    "currencies": ["EUR"],
                    "rates": {
                        "3 months": 1.75,
                        "6 months": 2.25,
                        "12 months": 2.75,
                        "2 years": {"<=500000": 2.25},
                        "3 years": {"<=500000": 2.00},
                        "4 years": {"<=500000": 2.00},
                        "5 years": {"<=500000": 2.00}
                    },
                    "min_amounts": {
                        "<=12 months": 10000,
                        ">12 months": 2500
                    },
                    "max_amounts": {
                        "<=12 months": 1000000,
                        ">12 months": 500000
                    },
                    "link": "https://www.ing.de/sparen-anlegen/sparen/festgeld/",
                    "logo": "img/ing_bank.png"
                },
                "Commerzbank": {
                    "currencies": ["EUR"],
                    "rates": {"EUR": 2.80},
                    "min_amount": 1000,
                    "max_amount": 100000,
                    "link": "https://www.commerzbank.de/sparen-anlegen/produkte/festgeld/",
                    "logo": "img/commerzbank.png"
                },
                "Deutsche Bank": {
                    "currencies": ["EUR"],
                    "rates": {"EUR": 3.00},
                    "min_amount": 2500,
                    "max_amount": 100000,
                    "link": "https://www.deutsche-bank.de/pk/sparen-und-anlegen/sparen/festzinssparen/festzinssparen-sea.html?kid=e.0400.03.80&gad_source=1&gclid=CjwKCAjw4ri0BhAvEiwA8oo6F_9bzXqmx1qT1LB6Qvc_OgI6W8wQ-7FapYnB0pOLkcA-Mb1OgAfyfxoCAa0QAvD_BwE",
                    "logo": "img/deutsche_bank.png"
                },
                "VR Bank": {
                    "currencies": ["EUR"],
                    "rates": {
                        "3 months": 2.30,
                        "6 months": 2.60,
                        "12 months": 3.00,
                        "2 years": 2.45,
                        "3 years": 2.20
                    },
                    "min_amount": 100,
                    "max_amount": float('inf'),
                    "link": "https://www.vrbanking.de/landingpage/lp-festgeld.landingpage.html?gad_source=1&gclid=CjwKCAjw4ri0BhAvEiwA8oo6F4zmhTdwZTwiVmYkXUQizk92MAHFdE7nQWpR08zEdsqk3y3kS-NxfRoCq3MQAvD_BwE",
                    "logo": "img/volksbank.png"
                },
                "Sparkasse": {
                    "currencies": ["EUR"],
                    "rates": {
                        "3 months": {"<=250000": 1.25, ">250000": 1.45},
                        "6 months": {"<=250000": 1.50, ">250000": 1.70},
                        "12 months": {"<=250000": 2.25, ">250000": 2.45},
                        "2 years": {"<=250000": 2.50, ">250000": 2.70},
                        "3 years": {"<=250000": 2.50, ">250000": 2.70},
                        "4 years": {"<=250000": 2.50, ">250000": 2.70},
                    },
                    "min_amount": 1,
                    "max_amount": float('inf'),
                    "link": "https://www.taunussparkasse.de/de/home/privatkunden/sparen-und-anlegen/festgeld.html?utm_campaign=Festgeld&utm_source=google&utm_medium=cpc&utm_campaign=Festgeld&utm_source=google&utm_medium=cpc&gad_source=1&pgs=direct&gclid=CjwKCAjw4ri0BhAvEiwA8oo6FxOoKSZE_e7gWYzShJEW8z_J_Jsot_uGGKU7I3cCnyQ5y4NOnVP6HhoCrxAQAvD_BwE&szsid=668e7ef0b74009548acd482b",
                    "logo": "img/sparkasse.png"
                }
            }

            # User interface
            # 使用 base64 编码嵌入图像 Embed images using base64 encoding

            def get_base64_image(image_path):
                with open(image_path, "rb") as image_file:
                    encoded_image = base64.b64encode(image_file.read()).decode()
                return encoded_image

            # 使用 HTML 和 CSS 在标题右侧添加图标 Add the icon to the right side of the title using HTML and CSS
            st.markdown(
                f"""
                <div style="display: flex; align-items: center;">
                    <h1>Bank Term Deposit Profit Calculator</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.divider()
            st.markdown(
                """
                <h2 class="custom-subheader">Use this tool to 🔍 compare fixed deposit options from various banks.</h2>
                """,
                unsafe_allow_html=True
            )


            # Select bank
            col1, col2 = st.columns([3, 1])
            with col1:
                selected_bank = st.selectbox("Choose Your Bank", list(banks.keys()))

            # Load and display the selected bank's logo
            logo_path = banks[selected_bank]["logo"]
            encoded_logo = get_base64_image(logo_path)

            with col2:
                if selected_bank == "VR Bank":
                    st.markdown(
                        f"""
                        <div style="display: flex; align-items: center; justify-content: center; height: 100%;">
                            <img src="data:image/png;base64,{encoded_logo}" style="max-width: 60%; height: auto;">
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""
                        <div style="display: flex; align-items: center; justify-content: center; height: 100%;">
                            <img src="data:image/png;base64,{encoded_logo}" style="max-width: 100%; max-height: 100px;">
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            # Display deposit conditions
            if selected_bank == "ING Bank":
                st.write(f"For {selected_bank} deposits, the amount must be more than {banks[selected_bank]['min_amounts']['<=12 months']} and no more than {banks[selected_bank]['max_amounts']['<=12 months']} for terms up to 12 months.")
                st.write(f"For {selected_bank} deposits, the amount must be more than {banks[selected_bank]['min_amounts']['>12 months']} and no more than {banks[selected_bank]['max_amounts']['>12 months']} for terms over 12 months.")
            else:
                min_amount = banks[selected_bank]["min_amount"]
                max_amount = banks[selected_bank]["max_amount"]
                if max_amount == float('inf'):
                    st.write(f"For {selected_bank} deposits, the amount must be more than {min_amount} with no upper limit.")
                else:
                    st.write(f"For {selected_bank} deposits, the amount must be more than {min_amount} and no more than {max_amount}")

            # Show bank's tarif table
            if selected_bank == "Commerzbank":
                data = [["1 year", f"{banks[selected_bank]['rates']['EUR']}%"]]
                rates_df = pd.DataFrame(data, columns=["Term", "Interest Rate (%)"])
                st.table(rates_df)
            elif selected_bank == "Deutsche Bank":
                data = [["1 year", f"{banks[selected_bank]['rates']['EUR']}%"]]
                rates_df = pd.DataFrame(data, columns=["Term", "Interest Rate (%)"])
                st.table(rates_df)
            elif selected_bank in ["VR Bank", "Sparkasse", "ING Bank"]:
                data = []
                for term, rate in banks[selected_bank]["rates"].items():
                    if isinstance(rate, dict):  # Handle tiered rates
                        data.append([term, f"{rate['<=500000']}%"] if selected_bank != "Sparkasse" else [term, f"{rate['<=250000']}%", f"{rate['>250000']}%"])
                    else:
                        data.append([term, f"{rate}%"])
                rates_df = pd.DataFrame(data, columns=["Term", "Interest Rate (%)"] if selected_bank != "Sparkasse" else ["Term", "Interest Rate (<=250000 EUR) %", "Interest Rate (>250000 EUR) %"])
                st.table(rates_df)
            else:
                rates_df = pd.DataFrame(list(banks[selected_bank]["rates"].items()), columns=["Currency", "Interest Rate (%)"])
                st.table(rates_df)


            # Input deposit duration 
            if selected_bank in ["VR Bank", "Sparkasse", "ING Bank"]:
                if selected_bank == "VR Bank":
                    term = st.selectbox("Select Deposit Term", ["3 months", "6 months", "12 months", "2 years", "3 years"])
                    if "months" in term:
                        years = int(term.split()[0]) / 12
                    else:
                        years = int(term.split()[0])
                elif selected_bank == "ING Bank":
                    term = st.selectbox("Select Deposit Term", ["3 months", "6 months", "12 months", "2 years", "3 years", "4 years", "5 years"])
                    years = {"3 months": 3/12, "6 months": 6/12, "12 months": 1, "2 years": 2, "3 years": 3, "4 years": 4, "5 years": 5}[term]
                else:
                    term = st.selectbox("Select Deposit Term", ["3 months", "6 months", "12 months", "2 years", "3 years", "4 years"])
                    years = {"3 months": 3/12, "6 months": 6/12, "12 months": 1, "2 years": 2, "3 years": 3, "4 years": 4}[term]
            else:
                years = st.number_input("Enter Deposit Duration (years)", min_value=1, value=1)

            # Select currency
            if len(banks[selected_bank]["currencies"]) == 1:
                currency = banks[selected_bank]["currencies"][0]
                st.write(f"Currency: {currency}")
            else:
                currency = st.selectbox("Select Currency", banks[selected_bank]["currencies"])

            # Input deposit amount
            if selected_bank == "ING Bank":
                if years <= 1:
                    min_amount = banks[selected_bank]['min_amounts']['<=12 months']
                    max_amount = banks[selected_bank]['max_amounts']['<=12 months']
                else:
                    min_amount = banks[selected_bank]['min_amounts']['>12 months']
                    max_amount = banks[selected_bank]['max_amounts']['>12 months']
            else:
                min_amount = banks[selected_bank]["min_amount"]
                max_amount = banks[selected_bank]["max_amount"]

            amount = st.number_input(f"Enter Deposit Amount ({currency})", min_value=min_amount, max_value=None if max_amount == float('inf') else int(max_amount), value=min_amount)

            # Calculate profit
            if st.button("Compute Profit"):
                if selected_bank == "VR Bank" or selected_bank == "ING Bank":
                    if isinstance(banks[selected_bank]["rates"][term], dict):
                        rate_category = "<=500000"
                        interest_rate = banks[selected_bank]["rates"][term][rate_category]
                    else:
                        interest_rate = banks[selected_bank]["rates"][term]
                elif selected_bank == "Sparkasse":
                    rate_category = "<=250000" if amount <= 250000 else ">250000"
                    interest_rate = banks[selected_bank]["rates"][term][rate_category]
                else:
                    interest_rate = banks[selected_bank]["rates"]["EUR"]
                
                profit = amount * (interest_rate / 100) * years
                st.write(f"The profit for a deposit of {amount} {currency} for {years} years at {selected_bank} is: {profit:.2f} {currency}")
                
                st.write("For more details, click [here]({}) to visit the bank's official website.".format(banks[selected_bank]["link"]))

            # Multi-select box for bank comparison
            st.markdown(
                f"""
                <h2 class="custom-subheader">Compare Bank Rates</h2>
                """,
                unsafe_allow_html=True
            )
            selected_banks = st.multiselect("Select Banks for Comparison", list(banks.keys()), default=[selected_bank])


            # Generate comparison chart
            if selected_banks:
                comparison_data = []
                for selected_bank in selected_banks:
                    if "EUR" in banks[selected_bank]["currencies"]:  # Only consider EUR currency
                        for term, rate in banks[selected_bank]["rates"].items():
                            if isinstance(rate, dict):  # For Sparkasse and ING Bank with tiered rates
                                comparison_data.append([selected_bank, term, rate["<=250000"] if "<=250000" in rate else rate["<=500000"]])
                                if ">250000" in rate:
                                    comparison_data.append([selected_bank, term, rate[">250000"]])
                            elif selected_bank in ["Deutsche Bank", "Commerzbank"]:
                                # Ensure constant rates are plotted across common terms for straight lines
                                for common_term in ["12 months"]:
                                    comparison_data.append([selected_bank, common_term, rate])
                            else:
                                comparison_data.append([selected_bank, term, rate])
                
                comparison_df = pd.DataFrame(comparison_data, columns=["Bank", "Term", "Interest Rate (%)"])
                
                # Filter terms to ensure they are valid time units
                valid_terms = ["3 months", "6 months", "12 months", "2 years", "3 years", "4 years", "5 years"]
                comparison_df = comparison_df[comparison_df["Term"].isin(valid_terms)]
                
                colors = {
                    "Deutsche Bank": "#0018A8",
                    "ING Bank": "#FF6200",
                    "Sparkasse": "red",
                    "Commerzbank": "#FFCC33",
                    "VR Bank": "#0066b3"
                }
                
                fig = px.line(comparison_df, x='Term', y='Interest Rate (%)', color='Bank', markers=True, title='Bank Rates Comparison',
                            color_discrete_map=colors)

                # Disconnect points for different banks to avoid unwanted lines
                fig.update_traces(connectgaps=False)

                st.plotly_chart(fig)
        
        else:
            st.warning("Upgrade to a Premium to access this function.")

    else:
        st.warning("Please log in to access this page.")
        st.stop()

if __name__ == "__main__":
    bank_page()
