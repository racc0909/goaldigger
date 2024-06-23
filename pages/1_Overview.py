import streamlit as st
import matplotlib.pyplot as plt

if not st.session_state.authentication_status:
    st.info('Please Login from the Home page and try again.')
    st.stop()

st.dataframe(st.session_state.df_userinfo, use_container_width=True, hide_index=True)

userinfo = st.session_state.df_userinfo.iloc[0]
st.dataframe(userinfo)

# --- INCOME FIG ---
incomes = [userinfo['regular_income'], userinfo['additional_income']]
labels1 = ['Regular Income', 'Additional Income']

fig1, ax1 = plt.subplots()
ax1.pie(incomes, labels = labels1, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.title("Income Chart")
st.pyplot(fig1)

# --- EXPENSES FIG ---
userinfo['leftover'] = userinfo['regular_income'] + userinfo['additional_income'] - userinfo['regular_expenses'] - userinfo['additional_expenses'] - userinfo['debt_expenses'] - userinfo['savings'] - userinfo['investments']
expenses = [userinfo['regular_expenses'], userinfo['additional_expenses'], userinfo['debt_expenses'], userinfo['savings'], userinfo['investments'], userinfo['leftover']]
labels2 = ['Regular Expenses', 'Additional Expenses', 'Debt Expenses', 'Savings', 'Investments', 'Left over']

fig2, ax2 = plt.subplots()
ax2.pie(expenses, labels = labels2, autopct='%1.1f%%', startangle=90)
ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.title("Expenses Chart")
st.pyplot(fig2)