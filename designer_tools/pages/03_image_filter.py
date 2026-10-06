from io import BytesIO

from PIL import Image, ImageEnhance, ImageFilter, ImageOps, UnidentifiedImageError
import streamlit as st


st.set_page_config(page_title="이미지 필터", page_icon="✨")
st.title("✨ 이미지 필터")
st.write("이미지를 업로드하고 필터를 적용한 뒤 결과를 다운로드하세요.")

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
        filter_name = st.selectbox(
            "필터 선택",
            ["원본", "흑백", "세피아", "블러", "선명하게"],
        )
        if filter_name == "흑백":
            result = ImageOps.grayscale(image).convert("RGB")
        elif filter_name == "세피아":
            grayscale = ImageOps.grayscale(image)
            result = ImageOps.colorize(
                grayscale,
                black="#3B2416",
                white="#F4D7A1",
            )
        elif filter_name == "블러":
            radius = st.slider("블러 강도", 1.0, 20.0, 5.0, 0.5)
            result = image.filter(ImageFilter.GaussianBlur(radius=radius))
        elif filter_name == "선명하게":
            result = ImageEnhance.Sharpness(image).enhance(2.5)
        else:
            result = image

        original_column, result_column = st.columns(2)
        with original_column:
            st.image(image, caption="원본", width="stretch")
        with result_column:
            st.image(result, caption=filter_name, width="stretch")

        output = BytesIO()
        result.save(output, format="PNG")
        st.download_button(
            "결과 이미지 다운로드",
            data=output.getvalue(),
            file_name="designer_filter.png",
            mime="image/png",
            width="stretch",
        )
