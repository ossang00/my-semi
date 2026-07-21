import pandas as pd
import streamlit as st


@st.cache_data
def load_data(path: str = "data.csv") -> pd.DataFrame:
    """산업통상부 반도체디스플레이 수출동향 추이 CSV를 불러와 전처리합니다."""
    df = pd.read_csv(path, encoding="utf-8-sig")
    df["년월"] = pd.to_datetime(df["년월"], format="%Y-%m")
    df = df.sort_values("년월").reset_index(drop=True)
    return df
