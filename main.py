# ── 그래프 4. 기간 일관객 TOP 10 ─────────────────────────────
st.divider()
st.header("4. 기간 일관객 TOP 10")

# 영화별 기간 일관객 합계와 10위권에 든 날짜 수를 계산합니다.
movie_summary = (
    df.groupby("영화명")
    .agg(
        기간_일관객=("일관객", "sum"),
        **{"10위권에_든_날수": ("날짜", "nunique")},
    )
    .reset_index()
)

# 기간 일관객 합계가 많은 TOP 10을 뽑습니다.
top10 = (
    movie_summary
    .sort_values("기간_일관객", ascending=False)
    .head(10)
    .sort_values("기간_일관객", ascending=True)
)

# 가로 막대그래프를 만듭니다.
fig4 = px.bar(
    top10,
    x="기간_일관객",
    y="영화명",
    orientation="h",
)

fig4.update_traces(
    hovertemplate=(
        "영화: %{y}"
        "<br>기간 일관객: %{x:,}명"
        "<br>10위권에 든 날수: %{customdata}일"
        "<extra></extra>"
    ),
    customdata=top10["10위권에_든_날수"],
)

fig4.update_layout(
    xaxis_title="기간 일관객 합계",
    yaxis_title="영화",
    showlegend=False,
)

st.plotly_chart(fig4, width="stretch")

st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")


# ── 그래프 5 ────────────────────────────────────────────────
st.divider()
st.header("5. 그래프 제목")

st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")

