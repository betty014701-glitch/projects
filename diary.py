import os
from calendar import monthcalendar
from datetime import date, timedelta

import pandas as pd
import streamlit as st


CSV_FILE = "diary.csv"
COLUMNS = ["날짜", "제목", "내용", "날씨", "기분", "먹은 음식"]

st.set_page_config(page_title="나의 일기장", page_icon="📔")
st.title("📔 나의 일기장")

today = date.today()
if "selected_date" not in st.session_state:
    st.session_state.selected_date = today
if "calendar_month" not in st.session_state:
    st.session_state.calendar_month = today.replace(day=1)

if os.path.exists(CSV_FILE):
    diaries = pd.read_csv(CSV_FILE, encoding="utf-8-sig")
    for column in COLUMNS:
        if column not in diaries.columns:
            diaries[column] = ""
    diaries = diaries[COLUMNS].fillna("")
else:
    diaries = pd.DataFrame(columns=COLUMNS)

with st.form("diary_form"):
    title = st.text_input("제목")
    content = st.text_area("내용", height=150)
    weather = st.selectbox("오늘의 날씨", ["맑음", "흐림", "비", "눈", "바람"])
    mood = st.selectbox(
        "오늘의 기분",
        ["아주 좋아요", "좋아요", "보통", "별로예요", "힘들어요"],
    )
    foods = st.text_area(
        "오늘 먹은 음식",
        height=100,
        placeholder="예: 아침 - 토스트, 점심 - 비빔밥",
    )
    save_diary = st.form_submit_button("저장")

if save_diary:
    new_entry = pd.DataFrame(
        [[today.isoformat(), title, content, weather, mood, foods]],
        columns=COLUMNS,
    )
    diaries = pd.concat([diaries, new_entry], ignore_index=True)
    diaries.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")
    st.session_state.selected_date = today
    st.session_state.calendar_month = today.replace(day=1)
    st.success("일기가 저장되었습니다.")

st.subheader("기록 달력")
month = st.session_state.calendar_month
previous_month, month_label, next_month = st.columns([1, 2, 1])
with previous_month:
    if st.button("‹ 이전 달", use_container_width=True):
        st.session_state.calendar_month = (month - timedelta(days=1)).replace(day=1)
        month = st.session_state.calendar_month
with month_label:
    st.markdown(
        f"<h3 style='text-align: center'>{month.year}년 {month.month}월</h3>",
        unsafe_allow_html=True,
    )
with next_month:
    if st.button("다음 달 ›", use_container_width=True):
        st.session_state.calendar_month = (month.replace(day=28) + timedelta(days=4)).replace(day=1)
        month = st.session_state.calendar_month

if diaries.empty:
    daily_counts = {}
else:
    diary_dates = pd.to_datetime(diaries["날짜"], errors="coerce")
    daily_counts = (
        diary_dates.dt.strftime("%Y-%m-%d")
        .value_counts()
        .to_dict()
    )

weekdays = st.columns(7)
for column, weekday in zip(weekdays, ["월", "화", "수", "목", "금", "토", "일"]):
    column.markdown(f"**{weekday}**")

for week in monthcalendar(month.year, month.month):
    day_columns = st.columns(7)
    for weekday_number, day in enumerate(week):
        with day_columns[weekday_number]:
            if day == 0:
                st.write("")
                continue
            calendar_date = date(month.year, month.month, day)
            date_key = calendar_date.isoformat()
            count = daily_counts.get(date_key, 0)
            if st.button(
                f"{day}\n📝 {count}건",
                key=f"calendar-{date_key}",
                type=(
                    "primary"
                    if calendar_date == st.session_state.selected_date
                    else "secondary"
                ),
                use_container_width=True,
            ):
                st.session_state.selected_date = calendar_date

selected_date = st.session_state.selected_date
st.subheader(f"{selected_date.year}년 {selected_date.month}월 {selected_date.day}일 기록")
if diaries.empty:
    selected_entries = diaries
else:
    selected_entries = diaries.loc[diary_dates.dt.date == selected_date]

st.caption(f"총 {len(selected_entries)}건")
if selected_entries.empty:
    st.write("이 날짜에는 기록이 없어요.")
else:
    for row_index, entry in selected_entries.iterrows():
        with st.container(border=True):
            entry_column, delete_column = st.columns([5, 1])
            with entry_column:
                st.write(f"**{entry['제목'] or '제목 없음'}**")
                st.caption(
                    f"기분: {entry['기분'] or '기록 없음'} · "
                    f"날씨: {entry['날씨'] or '기록 없음'}"
                )
                if entry["먹은 음식"]:
                    st.write(f"먹은 음식: {entry['먹은 음식']}")
                if entry["내용"]:
                    st.write(entry["내용"])
            with delete_column:
                if st.button(
                    "삭제",
                    key=f"delete-{row_index}",
                    use_container_width=True,
                ):
                    diaries = diaries.drop(index=row_index)
                    diaries.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")
                    st.rerun()
