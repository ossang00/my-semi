import streamlit as st
import plotly.graph_objects as go

from utils import load_data

st.set_page_config(page_title="품목별 비중 변화", page_icon="🧩", layout="wide")

st.title("🧩 품목별 비중 변화 추이")
st.caption("반도체 총액 대비 메모리 / 시스템반도체 / 개별소자 비중")

df = load_data()

df["메모리_비중"] = df["메모리(억불)"] / df["반도체(억불)"] * 100
df["시스템반도체_비중"] = df["시스템_반도체(억불)"] / df["반도체(억불)"] * 100
df["개별소자_비중"] = df["개별소자(억불)"] / df["반도체(억불)"] * 100

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=df["년월"], y=df["메모리_비중"], mode="lines", name="메모리",
        stackgroup="one", line=dict(width=0.5, color="#2563eb"),
    )
)
fig.add_trace(
    go.Scatter(
        x=df["년월"], y=df["시스템반도체_비중"], mode="lines", name="시스템반도체",
        stackgroup="one", line=dict(width=0.5, color="#dc2626"),
    )
)
fig.add_trace(
    go.Scatter(
        x=df["년월"], y=df["개별소자_비중"], mode="lines", name="개별소자",
        stackgroup="one", line=dict(width=0.5, color="#f59e0b"),
    )
)
fig.update_layout(
    height=520,
    hovermode="x unified",
    yaxis=dict(title="비중(%)", range=[0, 100]),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=10, r=10, t=40, b=10),
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("연도별 평균 비중")
yearly = (
    df.assign(연도=df["년월"].dt.year)
    .groupby("연도")[["메모리_비중", "시스템반도체_비중", "개별소자_비중"]]
    .mean()
    .round(1)
)
fig2 = go.Figure()
for col, name, color in [
    ("메모리_비중", "메모리", "#2563eb"),
    ("시스템반도체_비중", "시스템반도체", "#dc2626"),
    ("개별소자_비중", "개별소자", "#f59e0b"),
]:
    fig2.add_trace(go.Scatter(x=yearly.index, y=yearly[col], mode="lines+markers", name=name, line=dict(color=color)))
fig2.update_layout(
    height=420,
    yaxis=dict(title="평균 비중(%)"),
    xaxis=dict(title="연도", dtick=1),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=10, r=10, t=40, b=10),
)
st.plotly_chart(fig2, use_container_width=True)

st.dataframe(yearly.rename(columns={"메모리_비중": "메모리(%)", "시스템반도체_비중": "시스템반도체(%)", "개별소자_비중": "개별소자(%)"}), use_container_width=True)
