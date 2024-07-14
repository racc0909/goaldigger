import streamlit as st
import plotly.express as px
import pandas as pd
from db import showChosenPages
import os

showChosenPages()

# 加载 CSS 文件
def load_css(file_path):
    try:
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found: {file_path}")

# 使用相对路径或绝对路径加载 CSS 文件
css_file_path = os.path.join(os.getcwd(), "data/titlestyle.css")
load_css(css_file_path)

# 自定义CSS样式
st.markdown("""
    <style>
    .custom-box {
        border: 2px solid #478CCF; /* 边框颜色与主题一致 */
        border-radius: 10px;
        padding: 15px;
        margin: 10px;
        transition: all 0.3s ease-in-out;
        background-color: #FFFFFF; /* 背景颜色与主题一致 */
    }
    .custom-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    h2.custom-subheader {
        font-family: 'Montserrat', sans-serif;
        color: #478CCF;
        font-size: 24px;
    }
    h2 {
        font-size: 20px; /* 调整h2的字体大小 */
        color: #4535C1;
    }
    p, ul {
        font-family: 'sans serif';
        color: #3a4b53;
    }
    </style>
    """, unsafe_allow_html=True)

# 示例数据
data = {
    "Investment Option": [
        "Money Market Funds", "Short-term Government Bonds", "Certificates of Deposit (CDs)",
        "High-Yield Savings Accounts", "Intermediate-Term Government Bonds", "Corporate Bonds (High-Grade)",
        "Government Bonds", "Municipal Bonds", "Dividend-Paying Stocks", "Balanced Mutual Funds",
        "Corporate Bonds (Investment-Grade)", "Short-term Bond Funds", "Real Estate Investment Trusts (REITs)",
        "Diversified Stock Portfolios", "Individual Stocks", "Options Trading", "Cryptocurrencies",
        "Leveraged ETFs", "High-Yield Corporate Bonds (Junk Bonds)", "Mutual Funds/ETFs with Aggressive Growth",
        "Real Estate Investments", "Venture Capital and Private Equity", "High-Growth Mutual Funds/ETFs"
    ],
    "Duration (years)": [
        0.5, 1, 1, 1, 5, 5, 20, 20, 3, 4, 4, 2, 5, 10, 3, 0.5, 0.5, 0.25, 4, 4, 10, 10, 10
    ],
    "Expected Return (%)": [
        2, 3, 3.5, 1.5, 4, 5, 4, 5, 7, 6, 5, 4, 8, 9, 10, 15, 20, 15, 8, 9, 12, 20, 10
    ],
    "Risk Level (1-10)": [
        1, 1, 1, 1, 2, 3, 1, 2, 4, 3, 3, 3, 5, 6, 7, 10, 10, 9, 6, 7, 8, 10, 7
    ]
}

# 将数据转换为 DataFrame
df = pd.DataFrame(data)

# 页面标题
st.markdown(
    f"""
    <h1>Investment Options Comparison</h1>
    """,
    unsafe_allow_html=True
)


st.markdown(
    f"""
    <h2 class="custom-subheader">Discover and compare various investment options based on key factors like duration, expected return, and risk level. Customize your selections to find the best fit for your financial goals. Stay informed with real-time data and personalized recommendations.</h2>
    """,
    unsafe_allow_html=True
)


st.divider()
st.write("Select the investment options you want to compare:")

# 多选框供用户选择投资选项
options = st.multiselect(
    "Investment Options",
    df["Investment Option"].tolist(),
    default=df["Investment Option"].tolist()[:5]  # 默认选择前五个选项
)

# 过滤 DataFrame 以只包含所选投资选项
filtered_df = df[df["Investment Option"].isin(options)]

# 创建三维散点图
fig = px.scatter_3d(
    filtered_df,
    x="Duration (years)",
    y="Expected Return (%)",
    z="Risk Level (1-10)",
    color="Investment Option",
    title="Investment Options Comparison",
    labels={
        "Duration (years)": "Investment Duration (years)",
        "Expected Return (%)": "Expected Return (%)",
        "Risk Level (1-10)": "Risk Level (1-10)"
    },
    width=800,  # 宽度设置
    height=600  # 高度设置
)

# 在 Streamlit 页面中显示图表
st.plotly_chart(fig, use_container_width=True)

# 返回按钮
if st.button("Back to Assessment"):
    st.switch_page("pages/7_Risk_Tolerance_Assessment.py")

st.divider()

st.markdown(
    f"""
    <h2 class="custom-subheader">Exciting Updates Coming Soon!</h2>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <div class="custom-box">
        <h2>Thanks for using our Investment Options Comparison tool! 🎉 We will work hard to bring you even better features in the future:</h2>
        <ul>
            <li><b>Real-Time Data</b>: Get the latest market updates and stay ahead.</li>
            <li><b>Personalized Recommendations</b>: Tailored suggestions just for you.</li>
        </ul>
        <p>We'd love to hear your thoughts! 💬 What features would you like to see? Let us know and help us make this tool even better.</p>
    </div>
    """, unsafe_allow_html=True)

if st.button("I want to write some Feedback"):
    st.switch_page("pages/20_Share_Your_Feedback.py")
