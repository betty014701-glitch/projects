import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from color_utils import make_theme, rgb_to_hex, show_theme


st.set_page_config(page_title="컬러 피커", page_icon="🌈")
st.title("🌈 컬러 피커")
st.write("RGB 슬라이더를 움직여 색상을 선택하고 어울리는 컬러 테마를 확인하세요.")

red_column, green_column, blue_column = st.columns(3)
with red_column:
    red = st.slider("Red", 0, 255, 92, key="color_red")
with green_column:
    green = st.slider("Green", 0, 255, 122, key="color_green")
with blue_column:
    blue = st.slider("Blue", 0, 255, 235, key="color_blue")

hex_color = rgb_to_hex((red, green, blue))
st.markdown(
    f"""
    <div style="height:150px;border-radius:16px;background:{hex_color};
                border:1px solid #d1d5db"></div>
    """,
    unsafe_allow_html=True,
)
st.markdown(f"**선택한 색상:** `{hex_color}` · RGB({red}, {green}, {blue})")

st.subheader("컬러 테마")
show_theme(make_theme(hex_color))
