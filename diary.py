import os
from datetime import date

import pandas as pd
import streamlit as st


CSV_FILE = "diary.csv"
COLUMNS = ["날짜", "제목", "내용", "날씨"]

st.set_page_config(page_title="나의 일기장", page_icon="📔")
st.title("📔 나의 일기장")

title = st.text_input("제목")
content = st.text_area("내용", height=150)
weather = st.selectbox("오늘의 날씨", ["맑음", "흐림", "비", "눈", "바람"])

if st.button("저장"):
    new_entry = pd.DataFrame(
        [[date.today().isoformat(), title, content, weather]],
        columns=COLUMNS,
    )

    if os.path.exists(CSV_FILE):
        diaries = pd.read_csv(CSV_FILE, encoding="utf-8-sig")
        diaries = pd.concat([diaries, new_entry], ignore_index=True)
    else:
        diaries = new_entry

    diaries.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")
    st.success("일기가 저장되었습니다.")

st.subheader("저장된 일기")

if os.path.exists(CSV_FILE):
    diaries = pd.read_csv(CSV_FILE, encoding="utf-8-sig")
    st.dataframe(diaries, use_container_width=True)
else:
    st.write("아직 작성된 일기가 없어요.")
