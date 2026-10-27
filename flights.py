import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st


MONTHS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]

st.set_page_config(page_title="✈️ 항공 승객 분석", layout="wide")
st.title("✈️ 항공 승객 분석")

flights = sns.load_dataset("flights")
flights["month"] = pd.Categorical(flights["month"], categories=MONTHS, ordered=True)
flights["month_number"] = flights["month"].cat.codes + 1

total_rows = len(flights)
year_min = int(flights["year"].min())
year_max = int(flights["year"].max())
max_passengers = int(flights["passengers"].max())

metric_columns = st.columns(3)
metric_columns[0].metric("총 행 수", f"{total_rows:,}")
metric_columns[1].metric("연도 범위", f"{year_min}–{year_max}")
metric_columns[2].metric("최대 승객 수", f"{max_passengers:,}명")

month_range = st.sidebar.slider(
    "월 범위",
    min_value=1,
    max_value=12,
    value=(1, 12),
    format="%d월",
)

filtered_flights = flights[
    flights["month_number"].between(month_range[0], month_range[1])
]
yearly_average = (
    filtered_flights.groupby("year", as_index=False, observed=True)["passengers"]
    .mean()
    .sort_values("year")
)
yearly_average["3년 이동평균"] = yearly_average["passengers"].rolling(window=3).mean()
yearly_chart_data = yearly_average.melt(
    id_vars="year",
    value_vars=["passengers", "3년 이동평균"],
    var_name="구분",
    value_name="평균 승객 수",
)
yearly_chart_data["구분"] = yearly_chart_data["구분"].replace(
    {"passengers": "연도별 평균"}
)

st.subheader("연도별 평균 승객 수 및 3년 이동평균")
yearly_fig = px.line(
    yearly_chart_data,
    x="year",
    y="평균 승객 수",
    color="구분",
    line_dash="구분",
    line_dash_map={"연도별 평균": "solid", "3년 이동평균": "dash"},
    labels={"year": "연도"},
)
st.plotly_chart(yearly_fig, use_container_width=True)

monthly_average = (
    flights.groupby("month", as_index=False, observed=False)["passengers"]
    .mean()
    .sort_values("month")
)
st.subheader("월별 평균 승객 수")
monthly_bar_fig = px.bar(
    monthly_average,
    x="month",
    y="passengers",
    category_orders={"month": MONTHS},
    labels={"month": "월", "passengers": "평균 승객 수"},
)
st.plotly_chart(monthly_bar_fig, use_container_width=True)

st.subheader("월별 승객 수 분포")
monthly_box_fig = px.box(
    flights,
    x="month",
    y="passengers",
    category_orders={"month": MONTHS},
    labels={"month": "월", "passengers": "승객 수"},
)
st.plotly_chart(monthly_box_fig, use_container_width=True)

passenger_pivot = flights.pivot_table(
    index="year",
    columns="month",
    values="passengers",
    aggfunc="mean",
    observed=False,
).reindex(columns=MONTHS)
st.subheader("연도별·월별 승객 수 히트맵")
heatmap_fig = px.imshow(
    passenger_pivot,
    labels={"x": "월", "y": "연도", "color": "승객 수"},
    x=MONTHS,
    y=passenger_pivot.index,
    text_auto=True,
    color_continuous_scale="Blues",
    aspect="auto",
)
st.plotly_chart(heatmap_fig, use_container_width=True)
