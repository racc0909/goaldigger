import streamlit as st
from db import showChosenPages, logout

showChosenPages()

logout()

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 加载 CSS 文件
css_file_path = "data/titlestyle.css"
load_css(css_file_path)

# 页面标题
st.markdown(
    f"""
    <h1>Recommended Investment Options for Low Risk and Long Term</h1>
    """,
    unsafe_allow_html=True
)
st.divider()
# 描述
st.markdown(
    """
    Based on your <u>low</u> risk tolerance and preference for <u>long-term</u> investments, we recommend the following options:
    """,
    unsafe_allow_html=True
)

# 自定义CSS样式
st.markdown("""
    <style>
    .custom-box {
        border: 2px solid #cccccc;
        border-radius: 10px;
        padding: 15px;
        margin: 10px;
        transition: all 0.3s ease-in-out;
    }
    .custom-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .duration-bar, .return-bar {
        height: 10px;
        border-radius: 5px;
        margin-top: 5px;
        margin-left: 20px; /* 缩进与项目符号对齐 */
    }
    .duration-bar {
        background-color: #4CAF50; /* 绿色 */
    }
    .return-bar {
        background-color: #2196F3; /* 蓝色 */
    }
    </style>
    """, unsafe_allow_html=True)

# 推荐的投资选项
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="custom-box">
        <h2>1. Government Bonds</h2>
        <p>
        Government Bonds, especially long-term bonds, are debt securities issued by the government.
        They offer regular interest payments over a fixed period and are considered very safe.
        <ul>
            <li><b>Typical Duration</b>: 10 to 30 years</li>
            <div class="duration-bar" style="width: 90%;"></div>
            <li><b>Expected Return</b>: Low to moderate, but very safe</li>
            <div class="return-bar" style="width: 40%;"></div>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="custom-box">
        <h2>2. High-Yield Savings Accounts</h2>
        <p>
        High-Yield Savings Accounts offer higher interest rates than regular savings accounts while maintaining liquidity and safety.
        They are suitable for those who want to keep their funds accessible.
        <ul>
            <li><b>Typical Duration</b>: No fixed duration, accessible anytime</li>
            <div class="duration-bar" style="width: 90%;"></div>
            <li><b>Expected Return</b>: Higher than regular savings accounts, but lower than CDs</li>
            <div class="return-bar" style="width: 25%;"></div>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="custom-box">
        <h2>3. Certificates of Deposit (CDs)</h2>
        <p>
        Certificates of Deposit (CDs) are low-risk savings products offered by banks and credit unions.
        They offer a fixed interest rate for a specified term, making them a predictable and secure investment option.
        For long-term, consider CDs with longer terms.
        <ul>
            <li><b>Typical Duration</b>: 5 to 10 years</li>
            <div class="duration-bar" style="width: 90%;"></div>
            <li><b>Expected Return</b>: Higher than regular savings accounts, and can be quite attractive over long terms</li>
            <div class="return-bar" style="width: 40%;"></div>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="custom-box">
        <h2>4. Municipal Bonds</h2>
        <p>
        Municipal Bonds are debt securities issued by states, municipalities, or counties to finance public projects.
        They are often exempt from federal taxes, and sometimes state and local taxes as well.
        <ul>
            <li><b>Typical Duration</b>: 10 to 30 years</li>
            <div class="duration-bar" style="width: 90%;"></div>
            <li><b>Expected Return</b>: Moderate, with low risk and tax advantages</li>
            <div class="return-bar" style="width: 50%;"></div>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()
if st.button("Back to Assessment"):
    st.switch_page("pages/7_Risk_Tolerance_Assessment.py")

if st.button("I want to compare options"):
    st.switch_page("pages/18_options_comparison.py")

