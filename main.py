# 영화 데이터 그래프 도감 1 - 시간

import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# 페이지 설정
# ============================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide",
)

st.title("영화 데이터 그래프 도감 1 - 시간")


# ============================================================
# 데이터 불러오기
# ============================================================

DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/"
    "main/data/kobis_daily.csv"
)


@st.cache_data
def load_data():
    # 1년치(365일) 일별 박스오피스 10위권 기록을 불러옵니다.
    df = pd.read_csv(DATA_URL)

    # 여덟 자리 숫자로 된 날짜를 진짜 날짜(datetime)로 바꿉니다.
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce",
    )

    return df


df = load_data()


# ============================================================
# 그래프 1. 영화 하나의 흥행 곡선
# ============================================================

st.divider()

st.header("1. 한 영화의 흥행 곡선")

# 드롭다운으로 영화를 고릅니다.
movie_list = sorted(df["영화명"].dropna().unique())

movie = st.selectbox(
    "영화를 고르세요",
    movie_list,
)


one = (
    df[df["영화명"] == movie]
    .sort_values("날짜")
)


fig = px.line(
    one,
    x="날짜",
    y="일관객",
    markers=True,
    labels={
        "날짜": "날짜",
        "일관객": "일관객",
    },
    title=f"「{movie}」 날짜별 일관객 변화",
)


# 마우스를 올리면 날짜와 관객수가 보이도록 설정합니다.
fig.update_traces(
    hovertemplate=(
        "날짜 %{x|%Y-%m-%d}"
        "<br>"
        "관객 %{y:,}명"
        "<extra></extra>"
    )
)


st.plotly_chart(
    fig,
    width="stretch",
)


st.caption(
    "이 그래프로 알 수 있는 것: "
    "(한 문장으로 적어 보세요)"
)


# ============================================================
# 그래프 2. 일관객 합계가 가장 큰 영화 5편
# ============================================================

st.divider()

st.header("2. 일관객 합계가 가장 큰 영화 5편")

st.write(
    "전체 기간 동안 일관객의 합계가 가장 큰 5편을 골라 "
    "날짜별 일관객 변화를 비교합니다."
)


# ------------------------------------------------------------
# 전체 기간 영화별 일관객 합계 계산
# ------------------------------------------------------------

movie_totals = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
)


# 일관객 합계가 가장 큰 5편
top5_movies = movie_totals.head(5)["영화명"].tolist()


# ------------------------------------------------------------
# 상위 5편의 날짜별 데이터만 추출
# ------------------------------------------------------------

top5 = df[
    df["영화명"].isin(top5_movies)
].copy()


top5 = top5.sort_values(
    ["날짜", "영화명"]
)


# ------------------------------------------------------------
# Plotly 선 그래프
# ------------------------------------------------------------

fig2 = px.line(
    top5,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    labels={
        "날짜": "날짜",
        "일관객": "일관객",
        "영화명": "영화",
    },
    title="일관객 합계 상위 5편의 날짜별 일관객 변화",
)


# 마우스를 올리면 날짜, 영화명, 관객수가 표시됩니다.
fig2.update_traces(
    hovertemplate=(
        "날짜 %{x|%Y-%m-%d}"
        "<br>"
        "영화: %{fullData.name}"
        "<br>"
        "관객: %{y:,}명"
        "<extra></extra>"
    )
)


fig2.update_layout(
    height=550,
    hovermode="x unified",
    legend_title_text="영화",
)


st.plotly_chart(
    fig2,
    width="stretch",
)


st.caption(
    "이 그래프로 알 수 있는 것: "
    "(한 문장으로 적어 보세요)"
)


# ============================================================
# 앞으로 그래프 3, 4, 5가 이 아래에 추가됩니다.
# ============================================================

st.divider()

st.header("3. 다음 그래프")

st.info(
    "여기에 그래프 3을 추가하세요."
)

st.caption(
    "이 그래프로 알 수 있는 것: "
    "(한 문장으로 적어 보세요)"
)


st.divider()

st.header("4. 다음 그래프")

st.info(
    "여기에 그래프 4를 추가하세요."
)

st.caption(
    "이 그래프로 알 수 있는 것: "
    "(한 문장으로 적어 보세요)"
)


st.divider()

st.header("5. 다음 그래프")

st.info(
    "여기에 그래프 5를 추가하세요."
)

st.caption(
    "이 그래프로 알 수 있는 것: "
    "(한 문장으로 적어 보세요)"
)
