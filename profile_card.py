import streamlit as st


st.set_page_config(page_title="프로필 카드", page_icon="👤")

st.sidebar.header("프로필 입력")
name = st.sidebar.text_input("이름")
age = st.sidebar.slider("나이", min_value=1, max_value=100, value=20, step=1)
job = st.sidebar.selectbox("직업", ["개발자", "디자이너", "기획자", "마케터", "기타"])
certification = st.sidebar.text_input("자격증")
introduction = st.sidebar.text_area(
    "자기소개",
    placeholder="간단하게 소개해 주세요",
)
health_record = st.sidebar.text_area(
    "헬스 기록",
    placeholder="운동이나 건강 기록을 입력해 주세요",
)

st.title("프로필 카드")

with st.container(border=True):
    st.subheader(name or "이름을 입력해 주세요")
    st.write(f"**나이:** {age}세")
    st.write(f"**직업:** {job}")
    st.write(f"**자격증:** {certification or '없음'}")
    st.write("**자기소개**")
    st.write(introduction or "아직 소개가 없습니다.")
    st.write("**헬스 기록**")
    st.write(health_record or "아직 기록이 없습니다.")

if st.button("저장하기"):
    st.success("저장되었습니다! ✅")
