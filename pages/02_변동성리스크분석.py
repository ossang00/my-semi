import streamlit as st
import plotly.graph_objects as go

from utils import load_data

st.set_page_config(page_title="변동성·리스크 분석", page_icon="⚠️", layout="wide")

st.title("⚠️ 품목별 변동성·리스크 프로파일 분석")
st.caption("증감률 표준편차와 역대 최대 낙폭(Peak-to-Trough)으로 본 품목별 리스크")

df = load_data()

SEGMENTS = {
    "메모리": ("메모리(억불)", "메모리_전년동월대비_증감률(퍼센트)"),
    "시스템반도체": ("시스템_반도체(억불)", "시스템_반도체_전년동월대비_증감률(퍼센트)"),
    "개별소자": ("개별소자(억불)", "개별소자_전년동월대비_증감률(퍼센트)"),
    "디스플레이패널": ("디스플레이_패널(억불)", "디스플레이_패널_전년동월대비_증감률(퍼센트)"),
}


def max_drawdown(series):
    cummax = series.cummax()
    drawdown = (series - cummax) / cummax * 100
    return drawdown.min()


rows = []
for name, (value_col, growth_col) in SEGMENTS.items():
    std = df[growth_col].std()
    mdd = max_drawdown(df[value_col])
    rows.append({"품목": name, "YoY 변동성(표준편차, %p)": round(std, 1), "최대 낙폭(MDD, %)": round(mdd, 1)})

import pandas as pd
risk_df = pd.DataFrame(rows).sort_values("YoY 변동성(표준편차, %p)", ascending=False)

col1, col2 = st.columns(2)

with col1:
    st.subheader("변동성 순위 (증감률 표준편차)")
    fig1 = go.Figure(
        go.Bar(
            x=risk_df["YoY 변동성(표준편차, %p)"],
            y=risk_df["품목"],
            orientation="h",
            marker_color="#dc2626",
            text=risk_df["YoY 변동성(표준편차, %p)"],
            textposition="outside",
        )
    )
    fig1.update_layout(height=380, xaxis=dict(title="표준편차(%p)"), margin=dict(l=10, r=10, t=20, b=10))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("최대 낙폭(MDD) 비교")
    fig2 = go.Figure(
        go.Bar(
            x=risk_df["최대 낙폭(MDD, %)"],
            y=risk_df["품목"],
            orientation="h",
            marker_color="#2563eb",
            text=risk_df["최대 낙폭(MDD, %)"],
            textposition="outside",
        )
    )
    fig2.update_layout(height=380, xaxis=dict(title="MDD(%)"), margin=dict(l=10, r=10, t=20, b=10))
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.subheader("품목별 수출액 추이 (MDD 확인용)")
fig3 = go.Figure()
colors = {"메모리": "#2563eb", "시스템반도체": "#dc2626", "개별소자": "#f59e0b", "디스플레이패널": "#16a34a"}
for name, (value_col, _) in SEGMENTS.items():
    fig3.add_trace(go.Scatter(x=df["년월"], y=df[value_col], mode="lines", name=name, line=dict(color=colors[name])))
fig3.update_layout(
    height=460,
    hovermode="x unified",
    yaxis=dict(title="수출액(억불)"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=10, r=10, t=40, b=10),
)
st.plotly_chart(fig3, use_container_width=True)

st.dataframe(risk_df, use_container_width=True, hide_index=True)
st.caption("MDD(Max Drawdown)는 데이터 기간 내 누적 최고점 대비 최대 하락 비율입니다.")
