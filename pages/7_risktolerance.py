#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st

# 页面标题
st.title("Risk Tolerance Assessment")

# 获取用户输入的存款时间和金额
saving_time = st.slider("Select your saving time (in years):", min_value=1, max_value=30, value=5)
saving_amount = st.text_input("Enter your saving amount (€):", value="10000")

# 描述
st.write(f"So, you're planning to save {saving_amount} euros over {saving_time} years, huh? That's great! Now, let's talk about your risk tolerance. How bold are you feeling today? :)")

# 下拉菜单
risk_tolerance_options = [
    'Select your risk tolerance level',  # Placeholder
    'Low risk: I prefer to limit my exposure to risk, even if it means lower possible returns.',
    'Medium risk: I am open to more risk in pursuit of higher returns.',
    'High risk: I am comfortable with a higher level of risk to maximize potential returns.'
]

risk_tolerance = st.selectbox("Please select your level of risk tolerance:", risk_tolerance_options, index=0)

# 确定按钮
if st.button("Submit"):
    if risk_tolerance != 'Select your risk tolerance level':
        st.write(f"You selected: {risk_tolerance}")
        st.write(f"Great! You're saving {saving_amount} euros over {saving_time} years and you have a {risk_tolerance.split(':')[0]} tolerance to risk.")
    else:
        st.write("Please select a risk tolerance level.")

