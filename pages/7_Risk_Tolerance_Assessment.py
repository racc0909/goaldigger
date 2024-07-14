import streamlit as st
from db import getPlan, getUserInfo

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 加载 CSS 文件
css_file_path = "data/titlestyle.css"
load_css(css_file_path)

# 定义图标路径 Define the icon path
ICON_PATH_0_5 = "img/icon_0_5.png"

# 使用 base64 编码嵌入图像 Embed images using base64 encoding
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    return encoded_image

encoded_image = get_base64_image(ICON_PATH_0_5)

def editing_page():
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        user_id = st.session_state.user_id
        profile = getUserInfo(user_id)

        if 'invest_plan_id' in st.session_state:
            # Get plan info
            plan_id = st.session_state.invest_plan_id
            plan = getPlan(plan_id)
            saving_duration = plan.saving_duration
            goal_target = float(plan.goal_target)
        else:
            saving_duration = 12
            goal_target = 10000

        # 使用 HTML 和 CSS 在标题右侧添加图标 Add the icon to the right side of the title using HTML and CSS
        st.markdown(
            f"""
            <div style="display: flex; align-items: center;">
                <h1 style="margin: 0;">Risk Tolerance Assessment</h1>
                <img src="data:image/png;base64,{encoded_image}" width="40" style="margin-left: 10px;">
            </div>
            """,
            unsafe_allow_html=True
        )
        st.divider()
        # 使用st.expander隐藏特定部分
        with st.expander("You want to adjust the amount and time? Input your saving details here :)"):
            # 获取用户输入的存款时间和金额
            saving_time = st.slider("Select your saving time (in months):", min_value=1, max_value=360, value=saving_duration)
            saving_amount = st.number_input(f"Enter your saving amount ({profile.user_currency}):", min_value=0.0, format="%.2f", value=goal_target)

        # 描述
        # 使用自定义样式的子标题
        st.markdown(
            f"""
            <p class="custom-subheader">So, you're planning to save <span style="text-decoration: underline;">{saving_amount}</span> {profile.user_currency} over <span style="text-decoration: underline;">{saving_time}</span> months, huh? That's great! Now, let's talk about your risk tolerance. How bold are you feeling today? 😃</p>
            """,
            unsafe_allow_html=True
        )

        # 下拉菜单
        risk_tolerance_options = [
            '🟢 Low risk: I prefer to limit my exposure to risk, even if it means lower possible returns.',
            '🟡 Medium risk: I am open to more risk in pursuit of higher returns.',
            '🔴 High risk: I am comfortable with a higher level of risk to maximize potential returns.'
        ]

        risk_tolerance = st.selectbox("Please select your level of risk tolerance level 👉:", risk_tolerance_options, index=0)

        # 确定按钮
        if st.button("Submit"):
            if risk_tolerance == 'Select your risk tolerance level 👉':
                st.error("Please select a risk tolerance level.")
            else:
                st.write(f"You selected: {risk_tolerance}")
                st.write(f"Great! You're saving {saving_amount} {profile.user_currency} over {saving_time} months and you have a {risk_tolerance.split(':')[0]} tolerance to risk.")
                
                # 根据用户选择重定向到不同页面
                if saving_time <= 12:  # 短期投资
                    if risk_tolerance.startswith('🟢 Low risk'):
                        st.switch_page("pages/9_Low Risk, Short Term Investments.py")
                        st.experimental_rerun()
                    elif risk_tolerance.startswith('🟡 Medium risk'):
                        st.switch_page("pages/12_Medium Risk, Short Term Investments.py")
                        st.experimental_rerun()
                    elif risk_tolerance.startswith('🔴 High risk'):
                        st.switch_page("pages/15_High Risk, Short Term Investments.py")
                        st.experimental_rerun()
                elif 12 < saving_time <= 60:  # 中期投资
                    if risk_tolerance.startswith('🟢 Low risk'):
                        st.switch_page("pages/10_Low Risk, Medium Term Investments.py")
                        st.experimental_rerun()
                    elif risk_tolerance.startswith('🟡 Medium risk'):
                        st.switch_page("pages/13_Medium Risk, Medium Term Investments.py")
                        st.experimental_rerun()
                    elif risk_tolerance.startswith('🔴 High risk'):
                        st.switch_page("pages/16_High Risk, Medium Term Investments.py")
                        st.experimental_rerun()
                else:  # 长期投资
                    if risk_tolerance.startswith('🟢 Low risk'):
                        st.switch_page("pages/11_Low Risk, Long Term Investments.py")
                        st.experimental_rerun()
                    elif risk_tolerance.startswith('🟡 Medium risk'):
                        st.switch_page("pages/14_Medium Risk, Long Term Investments.py")
                        st.experimental_rerun()
                    elif risk_tolerance.startswith('🔴 High risk'):
                        st.switch_page("pages/17_High Risk, Long Term Investments.py")
                        st.experimental_rerun()

    else:
        st.warning("Please log in to access this page.")
        st.stop()

if __name__ == "__main__":
    editing_page()
