import colorsys
import math

import streamlit as st


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def make_theme(
    primary: str,
    secondary: str | None = None,
) -> dict[str, str]:
    red, green, blue = (int(primary[index : index + 2], 16) for index in (1, 3, 5))
    hue, saturation, value = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
    if secondary is None:
        accent_rgb = colorsys.hsv_to_rgb(
            (hue + 0.5) % 1,
            max(saturation, 0.45),
            max(value, 0.72),
        )
        secondary = rgb_to_hex(tuple(round(channel * 255) for channel in accent_rgb))

    luminance = (
        0.2126 * _linearize(red / 255)
        + 0.7152 * _linearize(green / 255)
        + 0.0722 * _linearize(blue / 255)
    )
    background = "#F4F6F8" if luminance < 0.45 else "#1F2937"
    return {
        "기본색": primary,
        "보조색": secondary,
        "배경색": background,
    }


def show_theme(theme: dict[str, str]) -> None:
    columns = st.columns(len(theme))
    for column, (label, color) in zip(columns, theme.items()):
        with column:
            st.markdown(
                f"""
                <div style="border:1px solid #d1d5db;border-radius:12px;
                            overflow:hidden;margin-bottom:8px">
                    <div style="height:88px;background:{color}"></div>
                    <div style="padding:12px">
                        <strong>{label}</strong><br>
                        <code>{color}</code>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _linearize(channel: float) -> float:
    if channel <= 0.04045:
        return channel / 12.92
    return math.pow((channel + 0.055) / 1.055, 2.4)
