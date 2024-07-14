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
    <h1>Recommended Investment Options for High Risk and Long Term</h1>
    """,
    unsafe_allow_html=True
)

st.divider()
# 描述
st.markdown(
    """
    Based on your <u>high</u> risk tolerance and preference for <u>long-term</u> investments, we recommend the following options:
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
        <h2>1. Individual Stocks</h2>
        <p>
        Investing in individual stocks can offer substantial returns over the long term.
        Selecting a diversified portfolio of high-growth companies can maximize returns but comes with higher risk.
        <ul>
            <li><b>Typical Duration</b>: 10 years or more</li>
            <div class="duration-bar" style="width: 90%;"></div>
            <li><b>Expected Return</b>: High, but with significant risk</li>
            <div class="return-bar" style="width: 80%;"></div>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="custom-box">
        <h2>2. Real Estate Investments</h2>
        <p>
        Directly investing in real estate properties can provide high returns through property value appreciation and rental income.
        This option requires active management and carries higher risk.
        <ul>
            <li><b>Typical Duration</b>: 10 years or more</li>
            <div class="duration-bar" style="width: 90%;"></div>
            <li><b>Expected Return</b>: High, with high risk and capital requirements</li>
            <div class="return-bar" style="width: 80%;"></div>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="custom-box">
        <h2>3. Venture Capital and Private Equity</h2>
        <p>
        Investing in venture capital and private equity involves providing capital to startups and private companies with high growth potential.
        These investments can offer significant returns but come with very high risk.
        <ul>
            <li><b>Typical Duration</b>: 10 years or more</li>
            <div class="duration-bar" style="width: 90%;"></div>
            <li><b>Expected Return</b>: Very high, but with very high risk</li>
            <div class="return-bar" style="width: 90%;"></div>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="custom-box">
        <h2>4. High-Growth Mutual Funds/ETFs</h2>
        <p>
        High-growth mutual funds and ETFs invest in companies with high growth potential.
        These funds are diversified but can be volatile.
        <ul>
            <li><b>Typical Duration</b>: 10 years or more</li>
            <div class="duration-bar" style="width: 90%;"></div>
            <li><b>Expected Return</b>: High, with higher volatility</li>
            <div class="return-bar" style="width: 80%;"></div>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()
if st.button("Back to Assessment"):
    st.switch_page("pages/7_Risk_Tolerance_Assessment.py")

if st.button("I want to compare options"):
    st.switch_page("pages/18_options_comparison.py")
