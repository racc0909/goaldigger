#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st

# 页面标题
st.title("Risk Tolerance Assessment")

# 使用st.expander隐藏特定部分
with st.expander("You want to adjust the amount and time? Input your saving details here :)"):
    # 获取用户输入的存款时间和金额
    saving_time = st.slider("Select your saving time (in months):", min_value=1, max_value=360, value=12)
    saving_amount = st.text_input("Enter your saving amount (€):", value="10000")

# 描述
st.write(f"So, you're planning to save {saving_amount} euros over {saving_time} months, huh? That's great! Now, let's talk about your risk tolerance. How bold are you feeling today? :)")

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
        st.write(f"Great! You're saving {saving_amount} euros over {saving_time} months and you have a {risk_tolerance.split(':')[0]} tolerance to risk.")
        
        # 根据用户选择重定向到不同页面
        if saving_time <= 12:  # 短期投资
            if risk_tolerance.startswith('Low risk'):
                st.switch_page("pages/9_lowshort.py")
                st.experimental_rerun()
            elif risk_tolerance.startswith('Medium risk'):
                st.switch_page("pages/10_lowmedium.py")
                st.experimental_rerun()
            elif risk_tolerance.startswith('High risk'):
                st.switch_page("pages/11_lowlong.py")
                st.experimental_rerun()
        elif 12 < saving_time <= 60:  # 中期投资
            if risk_tolerance.startswith('Low risk'):
                st.switch_page("pages/12_mediumshort.py")
                st.experimental_rerun()
            elif risk_tolerance.startswith('Medium risk'):
                st.switch_page("pages/13_mediummedium.py")
                st.experimental_rerun()
            elif risk_tolerance.startswith('High risk'):
                st.switch_page("pages/14_mediumlong.py")
                st.experimental_rerun()
        else:  # 长期投资
            if risk_tolerance.startswith('Low risk'):
                st.switch_page("pages/15_highshort.py")
                st.experimental_rerun()
            elif risk_tolerance.startswith('Medium risk'):
                st.switch_page("pages/16_highmedium.py")
                st.experimental_rerun()
            elif risk_tolerance.startswith('High risk'):
                st.switch_page("pages/17_highlong.py")
                st.experimental_rerun()
    else:
        st.write("Please select a risk tolerance level.")
