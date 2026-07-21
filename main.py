import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils import load_data

st.set_page_config(page_title="반도체 슈퍼사이클 구간 탐지", page_icon="📈", layout="wide")

st.title("📈 반도체 슈퍼사이클 구간 탐지")
st.caption("산업통상부 반도체·디스플레이 수출동향 추이 (2015.01 ~ 2025.12)")

df = load_data()

GROWTH_COL = "반도체_전년동월대비_증감률(퍼센트)"
VALUE_COL = "반도체(억불)"

# 상승기(증감률 > 0) / 하강기(증감률 <= 0) 구간 라벨링
df["국면"] = df[GROWTH_COL].apply(lambda x: "상승기" if x > 0 else "하강기")
df["구간ID"] = (df["국면"] != df["국면"].shift()).cumsum()

# 구간별 요약 테이블
segments = (
    df.groupby("구간ID")
    .agg(
        국면=("국면", "first"),
        시작월=("년월", "first"),
        종료월=("년월", "last"),
        개월수=("년월", "count"),
        시작액=(VALUE_COL, "first"),
        종료액=(VALUE_COL, "last"),
        최대증감률=(GROWTH_COL, "max"),
        최소증감률=(GROWTH_COL, "min"),
    )
    .reset_index(drop=True)
)
segments["누적변화율(%)"] = (
    (segments["종료액"] - segments["시작액"]) / segments["시작액"] * 100
).round(1)

# ── 그래프 ────────────────────────────────────────────────
fig = go.Figure()

# 국면 배경 음영
colors = {"상승기": "rgba(220,38,38,0.08)", "하강기": "rgba(37,99,235,0.08)"}
for _, seg in segments.iterrows():
    fig.add_vrect(
        x0=seg["시작월"],
        x1=seg["종료월"],
        fillcolor=colors[seg["국면"]],
        line_width=0,
        layer="below",
    )

fig.add_trace(
    go.Scatter(
        x=df["년월"],
        y=df[VALUE_COL],
        mode="lines",
        name="반도체 수출액(억불)",
        line=dict(color="#1f2937", width=2),
    )
)

fig.add_trace(
    go.Scatter(
        x=df["년월"],
        y=df[GROWTH_COL],
        mode="lines",
        name="전년동월대비 증감률(%)",
        line=dict(color="#dc2626", width=1.5, dash="dot"),
        yaxis="y2",
    )
)

fig.update_layout(
    height=560,
    hovermode="x unified",
    yaxis=dict(title="수출액(억불)"),
    yaxis2=dict(title="증감률(%)", overlaying="y", side="right", showgrid=False),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=10, r=10, t=40, b=10),
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("구간별 요약")
st.dataframe(
    segments.rename(
        columns={
            "국면": "국면",
            "시작월": "시작",
            "종료월": "종료",
            "개월수": "지속(개월)",
            "시작액": "시작 수출액(억불)",
            "종료액": "종료 수출액(억불)",
            "최대증감률": "최대 YoY(%)",
            "최소증감률": "최소 YoY(%)",
        }
    ),
    use_container_width=True,
    hide_index=True,
)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("전체 구간 수", f"{segments.shape[0]}개")
with col2:
    up = segments[segments["국면"] == "상승기"]["개월수"].mean()
    st.metric("평균 상승기 길이", f"{up:.1f}개월" if pd.notna(up) else "-")
with col3:
    down = segments[segments["국면"] == "하강기"]["개월수"].mean()
    st.metric("평균 하강기 길이", f"{down:.1f}개월" if pd.notna(down) else "-")

st.caption("국면 정의: 전년동월대비 증감률이 양수(+)면 상승기, 0 이하면 하강기로 분류했습니다.")
