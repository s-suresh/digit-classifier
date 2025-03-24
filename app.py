import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageOps
import numpy as np

st.title("Improved Drawing Clarity")

canvas_result = st_canvas(
    fill_color="black",
    stroke_width=8,  # Moderate stroke for better clarity
    stroke_color="white",
    background_color="black",
    height=560,  # Larger canvas for better resolution
    width=560,
    drawing_mode="freedraw",
    key="canvas"
)

if "image_index" not in st.session_state:
    st.session_state.image_index = 0

if st.button("Save as PNG"):
    if canvas_result.image_data is not None:
        img = Image.fromarray((canvas_result.image_data[:, :, :3]).astype(np.uint8))  # Remove alpha
        img = img.convert("L")  # Convert to grayscale
        img = ImageOps.invert(img)  # Ensure black drawing on white background
        img = img.resize((28, 28), Image.LANCZOS)  # Downscale with anti-aliasing
        img.save(f"{st.session_state.image_index}.png")
        st.session_state.image_index += 1
        st.success(f"Image saved as {st.session_state.image_index - 1}.png")

if st.button("Retry"):
    st.rerun()
