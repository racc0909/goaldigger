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
    <h1>Recommended Investment Options for Medium Risk and Short Term</h1>
    """,
    unsafe_allow_html=True
)
st.divider()
# 描述
st.markdown(
    f"""
    <h2 class="custom-subheader">Based on your <u>medium</u> risk tolerance and preference for <u>short-term</u> investments, we recommend the following options:</h2>
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
        <h2>1. Dividend-Paying Stocks</h2>
        <p>
        Dividend-paying stocks provide regular income through dividends and potential for capital appreciation.
        They can be more volatile than bonds but offer higher returns.
        <ul>
            <li><b>Typical Duration</b>: 1 to 3 years</li>
            <div class="duration-bar" style="width: 30%;"></div>
            <li><b>Expected Return</b>: Moderate to high, with moderate risk</li>
            <div class="return-bar" style="width: 60%;"></div>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="custom-box">
        <h2>2. Balanced Mutual Funds</h2>
        <p>
        Balanced mutual funds invest in a mix of stocks and bonds, aiming to balance risk and return.
        They are less volatile than pure equity funds and suitable for short-term investment horizons.
        <ul>
            <li><b>Typical Duration</b>: 1 to 3 years</li>
            <div class="duration-bar" style="width: 30%;"></div>
            <li><b>Expected Return</b>: Moderate, with a balanced risk profile</li>
            <div class="return-bar" style="width: 50%;"></div>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="custom-box">
        <h2>3. Corporate Bonds (Investment-Grade)</h2>
        <p>
        Investment-grade corporate bonds are issued by financially stable companies and offer higher returns than government bonds.
        They come with moderate risk and are suitable for short-term investments.
        <ul>
            <li><b>Typical Duration</b>: 1 to 3 years</li>
            <div class="duration-bar" style="width: 30%;"></div>
            <li><b>Expected Return</b>: Moderate, with relatively low risk compared to lower-grade corporate bonds</li>
            <div class="return-bar" style="width: 45%;"></div>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="custom-box">
        <h2>4. Short-term Bond Funds</h2>
        <p>
        Short-term bond funds invest in bonds with short maturities, reducing interest rate risk.
        They offer higher returns than money market funds but come with moderate risk.
        <ul>
            <li><b>Typical Duration</b>: 1 to 3 years</li>
            <div class="duration-bar" style="width: 30%;"></div>
            <li><b>Expected Return</b>: Moderate, with lower risk than longer-term bond funds</li>
            <div class="return-bar" style="width: 50%;"></div>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)
st.write("Please note, these are general recommendations and not personalized advice.")
st.divider()
if st.button("Back to Assessment"):
    st.switch_page("pages/7_Risk_Tolerance_Assessment.py")

if st.button("I want to compare options"):
    st.switch_page("pages/18_options_comparison.py")

