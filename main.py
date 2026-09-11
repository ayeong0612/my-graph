import pandas as pd
import plotly.express as px
import streamlit as st


# =========================================================
# 페이지 설정
# =========================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide",
)


# =========================================================
# 제목
# =========================================================

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")

st.write(
    "1년치 일별 박스오피스 데이터를 이용해서 "
    "영화의 시간에 따른 변화를 그래프로 살펴봅니다."
)


# =========================================================
# 데이터 불러오기
# =========================================================

DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/"
    "main/data/kobis_daily.csv"
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜 열을 진짜 날짜(datetime)로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce",
    )

    # 숫자형 열 변환
    numeric_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    return df


try:
    df = load_data()

except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.error(f"오류 내용: {e}")
    st.stop()


# =========================================================
# 데이터 기본 정리
# =========================================================

df = df.dropna(subset=["날짜", "영화명", "일관객"])

df["영화명"] = df["영화명"].astype(str).str.strip()

# 영화명 목록
movie_list = sorted(df["영화명"].unique())


# =========================================================
# 그래프 1
# 영화별 날짜에 따른 일관객 변화
# =========================================================

st.divider()

st.header("📈 그래프 1. 영화별 날짜에 따른 일관객 변화")

st.write(
    "영화를 하나 선택하면 해당 영화의 날짜별 일관객 변화를 "
    "선 그래프로 확인할 수 있습니다."
)

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list,
)


# 선택한 영화의 데이터만 추출
movie_df = df[df["영화명"] == selected_movie].copy()

# 날짜순으로 정렬
movie_df = movie_df.sort_values("날짜")


# ---------------------------------------------------------
# Plotly 선 그래프
# ---------------------------------------------------------

fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"「{selected_movie}」 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
    },
)


# 마우스를 올렸을 때 날짜와 관객수가 표시되도록 설정
fig.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)


fig.update_layout(
    hovermode="x unified",
    height=500,
    margin=dict(
        l=20,
        r=20,
        t=70,
        b=20,
    ),
)


st.plotly_chart(
    fig,
    use_container_width=True,
)


# =========================================================
# 이 그래프로 알 수 있는 것
# =========================================================

st.subheader("💡 이 그래프로 알 수 있는 것")

st.info(
    "여기에 이 그래프를 보고 알 수 있는 내용을 한 문장으로 작성하세요."
)


# =========================================================
# 다음 그래프를 위한 구역
# =========================================================

st.divider()

st.header("📊 그래프 2")

st.info(
    "다음 그래프를 이곳에 추가하세요."
)


# =========================================================
# 그래프 3 이후도 아래에 계속 추가
# =========================================================

# st.divider()
# st.header("📊 그래프 3")
#
# 여기에 새로운 그래프를 추가하세요.
#
# st.subheader("💡 이 그래프로 알 수 있는 것")
# st.info("여기에 설명을 작성하세요.")
