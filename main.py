# 영화 데이터 그래프 도감 1 - 시간
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")
st.title("영화 데이터 그래프 도감 1 - 시간")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    # 1년치(365일) 일별 박스오피스 10위권 기록을 불러옵니다.
    df = pd.read_csv(DATA_URL)

    # 여덟 자리 숫자로 된 날짜를 진짜 날짜로 바꿉니다.
    df["날짜"] = pd.to_datetime(df["날짜"], format="%Y%m%d")

    return df


df = load_data()


# ── 그래프 1. 영화 하나의 흥행 곡선 ──────────────────────────
st.header("1. 한 영화의 흥행 곡선")

movie_list = sorted(df["영화명"].dropna().unique())
movie = st.selectbox("영화를 고르세요", movie_list)

one = df[df["영화명"] == movie].sort_values("날짜")

fig = px.line(
    one,
    x="날짜",
    y="일관객",
    markers=True,
)

fig.update_traces(
    hovertemplate="날짜 %{x|%Y-%m-%d}<br>관객 %{y:,}명<extra></extra>"
)

st.plotly_chart(fig, width="stretch")

st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")


# ── 그래프 2. 기간 전체 일관객 합계가 가장 큰 영화 5편 ────────
st.divider()
st.header("2. 일관객 합계가 가장 큰 영화 5편")

movie_totals = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
)

top5_movies = movie_totals.head(5)["영화명"].tolist()

top5 = (
    df[df["영화명"].isin(top5_movies)]
    .sort_values(["날짜", "영화명"])
)

fig2 = px.line(
    top5,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
)

fig2.update_traces(
    hovertemplate=(
        "영화: %{fullData.name}"
        "<br>날짜: %{x|%Y-%m-%d}"
        "<br>관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    hovermode="closest",
    legend_title_text="영화",
)

st.plotly_chart(fig2, width="stretch")

st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")


# ── 그래프 3. 날짜별 10위권 일관객 합계 ───────────────────────
st.divider()
st.header("3. 날짜별 10위권 일관객 합계")

# 날짜별로 그날의 10위권 영화 일관객을 모두 합칩니다.
daily_audience = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

daily_audience = daily_audience.rename(
    columns={"일관객": "10위권_일관객_합계"}
)

# 합계가 가장 큰 날 3일을 찾습니다.
top3_days = daily_audience.nlargest(3, "10위권_일관객_합계")

# 영역 그래프를 만듭니다.
fig3 = px.area(
    daily_audience,
    x="날짜",
    y="10위권_일관객_합계",
)

# 상위 3일을 그래프 위에 표시합니다.
fig3.add_scatter(
    x=top3_days["날짜"],
    y=top3_days["10위권_일관객_합계"],
    mode="markers+text",
    text=top3_days["날짜"].dt.strftime("%Y-%m-%d"),
    textposition="top center",
    marker=dict(
        size=10,
        color="red",
    ),
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>10위권 합계: %{y:,}명"
        "<extra></extra>"
    ),
    name="합계 상위 3일",
)

fig3.update_traces(
    selector=dict(type="scatter", mode="lines"),
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>10위권 합계: %{y:,}명"
        "<extra></extra>"
    ),
)

fig3.update_layout(
    xaxis_title="날짜",
    yaxis_title="10위권 일관객 합계",
    showlegend=False,
)

st.plotly_chart(fig3, width="stretch")

st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")


# ── 앞으로 그래프 4, 5가 이 아래에 추가됩니다 ──────────────
st.divider()
st.header("4. 그래프 제목")

st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")


st.divider()
st.header("5. 그래프 제목")

st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")

