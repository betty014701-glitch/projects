import streamlit as st


st.set_page_config(page_title="디자이너 컬러 스튜디오", page_icon="🎨", layout="wide")

st.title("🎨 디자이너 컬러 스튜디오")
st.write("색을 탐색하고, 이미지에서 팔레트를 찾고, 사진에 필터를 적용해 보세요.")

apps = [
    (
        "🌈",
        "컬러 피커",
        "RGB 값을 조절해 나만의 컬러와 어울리는 테마를 만들어 보세요.",
        "pages/01_color_picker.py",
        "컬러 피커 열기",
    ),
    (
        "🖼️",
        "이미지 컬러 추출",
        "이미지에서 가장 눈에 띄는 색상 다섯 가지를 찾아보세요.",
        "pages/02_image_color.py",
        "팔레트 추출하기",
    ),
    (
        "✨",
        "이미지 필터",
        "흑백, 세피아, 블러 필터를 적용하고 결과를 저장해 보세요.",
        "pages/03_image_filter.py",
        "필터 적용하기",
    ),
]

columns = st.columns(3)
for column, (icon, title, description, page, link_label) in zip(columns, apps):
    with column:
        with st.container(border=True):
            st.subheader(f"{icon} {title}")
            st.write(description)
            st.page_link(page, label=link_label, icon=icon, width="stretch")
