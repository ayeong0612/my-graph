import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 1 - 시간")


DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    df["날짜"] = pd.to_datetime(df["날짜"], format="%Y%m%d")
    return df


df = load_data()


# ─────────────────────────────────────────────
# 그래프 1
# ─────────────────────────────────────────────

st.header("1. 한 영화의 흥행 곡선")

movie_list = sorted(df["영화명"].dropna().unique())
movie = st.selectbox("영화를 고르세요", movie_list)

one = df[df["영화명"] == movie].sort_values("날짜")

fig1 = px.line(
    one,
    x="날짜",
    y="일관객",
    markers=True
)

fig1.update_traces(
    hovertemplate=(
        "날짜 %{x|%Y-%m-%d}"
        "<br>관객 %{y:,}명"
        "<extra></extra>"
    )
)

st.plotly_chart(fig1, width="stretch")

st.caption(
    "이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)"
)


# ─────────────────────────────────────────────
# 그래프 2
# ─────────────────────────────────────────────

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
    markers=True
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
    legend_title_text="영화"
)

st.plotly_chart(fig2, width="stretch")

st.caption(
    "이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)"
)


# ─────────────────────────────────────────────
# 그래프 3
# ─────────────────────────────────────────────

st.divider()
st.header("3. 날짜별 10위권 일관객 합계")

daily_audience = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

daily_audience = daily_audience.rename(
    columns={"일관객": "10위권_일관객_합계"}
)

top3_days = daily_audience.nlargest(
    3,
    "10위권_일관객_합계"
)

fig3 = px.area(
    daily_audience,
    x="날짜",
    y="10위권_일관객_합계"
)

fig3.add_scatter(
    x=top3_days["날짜"],
    y=top3_days["10위권_일관객_합계"],
    mode="markers+text",
    text=top3_days["날짜"].dt.strftime("%Y-%m-%d"),
    textposition="top center",
    marker=dict(
        size=10,
        color="red"
    ),
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>10위권 합계: %{y:,}명"
        "<extra></extra>"
    ),
    name="합계 상위 3일"
)

fig3.update_layout(
    xaxis_title="날짜",
    yaxis_title="10위권 일관객 합계",
    showlegend=False
)

st.plotly_chart(fig3, width="stretch")

st.caption(
    "이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)"
)


# ─────────────────────────────────────────────
# 그래프 4
# ─────────────────────────────────────────────

st.divider()
st.header("4. 기간 일관객 TOP 10")

movie_summary = (
    df.groupby("영화명")
    .agg(
        기간_일관객=("일관객", "sum"),
        **{"10위권에_든_날수": ("날짜", "nunique")}
    )
    .reset_index()
)

top10 = (
    movie_summary
    .sort_values("기간_일관객", ascending=False)
    .head(10)
    .sort_values("기간_일관객", ascending=True)
)

fig4 = px.bar(
    top10,
    x="기간_일관객",
    y="영화명",
    orientation="h"
)

fig4.update_traces(
    customdata=top10["10위권에_든_날수"],
    hovertemplate=(
        "영화: %{y}"
        "<br>기간 일관객: %{x:,}명"
        "<br>10위권에 든 날수: %{customdata}일"
        "<extra></extra>"
    )
)

fig4.update_layout(
    xaxis_title="기간 일관객 합계",
    yaxis_title="영화",
    showlegend=False
)

st.plotly_chart(fig4, width="stretch")

st.caption(
    "이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)"
)


# ─────────────────────────────────────────────
# 그래프 5
# ─────────────────────────────────────────────

st.divider()
st.header("5. 월 × 요일별 일관객 합계")

heatmap_df = df.copy()

heatmap_df["월"] = heatmap_df["날짜"].dt.month

weekday_names = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일"
]

heatmap_df["요일"] = heatmap_df["날짜"].dt.weekday.map(
    dict(enumerate(weekday_names))
)

heatmap = (
    heatmap_df
    .pivot_table(
        index="월",
        columns="요일",
        values="일관객",
        aggfunc="sum",
        fill_value=0
    )
    .reindex(columns=weekday_names)
)

fig5 = px.imshow(
    heatmap,
    color_continuous_scale="Blues",
    labels={
        "x": "요일",
        "y": "월",
        "color": "일관객 합계"
    },
    aspect="auto",
    text_auto=","
)

fig5.update_traces(
    hovertemplate=(
        "%{y}월 %{x}"
        "<br>일관객 합계: %{z:,}명"
        "<extra></extra>"
    )
)

fig5.update_layout(
    xaxis_title="요일",
    yaxis_title="월",
    coloraxis_colorbar_title="일관객"
)

st.plotly_chart(fig5, width="stretch")

st.caption(
    "이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)"
)

