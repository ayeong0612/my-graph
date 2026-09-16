# ── 그래프 5. 월 × 요일별 일관객 합계 히트맵 ─────────────────
st.divider()
st.header("5. 월 × 요일별 일관객 합계")

# 날짜에서 월과 요일을 뽑습니다.
heatmap_df = df.copy()

heatmap_df["월"] = heatmap_df["날짜"].dt.month

weekday_names = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일",
]

# pandas의 weekday는 월요일=0, 일요일=6입니다.
heatmap_df["요일"] = heatmap_df["날짜"].dt.weekday.map(
    dict(enumerate(weekday_names))
)

# 월 × 요일별 일관객 합계를 계산합니다.
heatmap = (
    heatmap_df
    .pivot_table(
        index="월",
        columns="요일",
        values="일관객",
        aggfunc="sum",
        fill_value=0,
    )
    .reindex(columns=weekday_names)
)

# 히트맵을 만듭니다.
fig5 = px.imshow(
    heatmap,
    color_continuous_scale="Blues",
    labels={
        "x": "요일",
        "y": "월",
        "color": "일관객 합계",
    },
    aspect="auto",
    text_auto=",",
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
    coloraxis_colorbar_title="일관객",
)

st.plotly_chart(fig5, width="stretch")

st.caption(
    "이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)"
)


st.caption(
    "이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)"
)
