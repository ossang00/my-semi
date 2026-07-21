import streamlit as st
import plotly.graph_objects as go

from utils import load_data

st.set_page_config(page_title="메모리 내부 구성 변화", page_icon="💾", layout="wide")

st.title("💾 메모리 내부 구성(D램 / 낸드 / MCP) 변화")
st.caption("전체 반도체 수출액 대비 D램·낸드·MCP 비중과 변동성 비교")

df = load_data()

df["D램_비중"] = df["메모리_D램(억불)"] / df["반도체(억불)"] * 100
df["낸드_비중"] = df["메모리_낸드(억불)"] / df["반도체(억불)"] * 100
df["MCP_비중"] = df["메모리_MCP(억불)"] / df["반도체(억불)"] * 100

fig = go.Figure()
for col, name, color in [
    ("D램_비중", "D램", "#2563eb"),
    ("낸드_비중", "낸드", "#16a34a"),
    ("MCP_비중", "MCP", "#f59e0b"),
]:
    fig.add_trace(go.Scatter(x=df["년월"], y=df[col], mode="lines", name=name, line=dict(color=color, width=2)))
fig.update_layout(
    height=520,
    hovermode="x unified",
    yaxis=dict(title="반도체 총액 대비 비중(%)"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=10, r=10, t=40, b=10),
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("연도별 평균 비중 추이")
yearly = (
    df.assign(연도=df["년월"].dt.year)
    .groupby("연도")[["D램_비중", "낸드_비중", "MCP_비중"]]
    .mean()
    .round(1)
)
fig3 = go.Figure()
for col, name, color in [
    ("D램_비중", "D램", "#2563eb"),
    ("낸드_비중", "낸드", "#16a34a"),
    ("MCP_비중", "MCP", "#f59e0b"),
]:
    fig3.add_trace(go.Scatter(x=yearly.index, y=yearly[col], mode="lines+markers", name=name, line=dict(color=color)))
fig3.update_layout(
    height=380,
    yaxis=dict(title="평균 비중(%)"),
    xaxis=dict(title="연도", dtick=1),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=10, r=10, t=20, b=10),
)
st.plotly_chart(fig3, use_container_width=True)
st.caption("품목별 변동성·리스크(표준편차, 최대낙폭) 비교는 '변동성·리스크 분석' 페이지에서 확인하실 수 있습니다.")

col1, col2, col3 = st.columns(3)
recent = df.tail(12)
with col1:
    st.metric("최근 12개월 평균 D램 비중", f"{recent['D램_비중'].mean():.1f}%")
with col2:
    st.metric("최근 12개월 평균 낸드 비중", f"{recent['낸드_비중'].mean():.1f}%")
with col3:
    st.metric("최근 12개월 평균 MCP 비중", f"{recent['MCP_비중'].mean():.1f}%")
