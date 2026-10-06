from io import BytesIO
import sys
from pathlib import Path

from PIL import Image, UnidentifiedImageError
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from color_utils import make_theme, show_theme


st.set_page_config(page_title="이미지 컬러 추출", page_icon="🖼️")
st.title("🖼️ 이미지 컬러 추출")
st.write("이미지를 업로드하면 주요 색상 다섯 가지와 이를 활용한 테마를 보여줍니다.")

uploaded_file = st.file_uploader(
    "이미지 업로드",
    type=["png", "jpg", "jpeg", "webp"],
)

if uploaded_file is not None:
    try:
        image = Image.open(BytesIO(uploaded_file.getvalue())).convert("RGB")
    except (UnidentifiedImageError, OSError) as error:
        st.error(f"이미지를 열 수 없습니다. 다른 이미지 파일을 선택해 주세요. ({error})")
    else:
        st.image(image, caption=uploaded_file.name, width="stretch")
        sample = image.copy()
        sample.thumbnail((400, 400))
        quantized = sample.quantize(colors=5, method=Image.Quantize.MEDIANCUT)
        palette = quantized.getpalette()
        colors = quantized.getcolors(maxcolors=256) or []
        colors.sort(reverse=True)
        top_colors = [
            "#{:02X}{:02X}{:02X}".format(*palette[index * 3 : index * 3 + 3])
            for _, index in colors[:5]
        ]

        if not top_colors:
            st.error("이미지에서 색상을 추출하지 못했습니다.")
        else:
            st.subheader("주요 색상")
            swatches = st.columns(5)
            for index, column in enumerate(swatches):
                if index < len(top_colors):
                    color = top_colors[index]
                    with column:
                        st.markdown(
                            f"""
                            <div style="height:90px;background:{color};
                                        border-radius:12px;border:1px solid #d1d5db"></div>
                            <div style="text-align:center;padding-top:8px">
                                <code>{color}</code>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

            if len(top_colors) < 5:
                st.info(
                    f"이미지에서 구별되는 색상이 {len(top_colors)}개라 "
                    "확인된 색상만 표시했습니다."
                )

            st.subheader("이미지 컬러 테마")
            secondary = top_colors[1] if len(top_colors) > 1 else None
            show_theme(make_theme(top_colors[0], secondary))
