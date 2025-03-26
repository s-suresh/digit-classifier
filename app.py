import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageOps
import numpy as np
import tensorflow as tf

# Load trained model
@st.cache_resource()
def load_model():
    return tf.keras.models.load_model("model.h5")

model = load_model()

st.title("Handwritten Digit Classifier")

canvas_result = st_canvas(
    fill_color="white",
    stroke_width=8,
    stroke_color="black",
    background_color="white",
    height=560,
    width=560,
    drawing_mode="freedraw",
    key="canvas"
)

if "image_index" not in st.session_state:
    st.session_state.image_index = 0

if st.button("Classify Drawing"):
    if canvas_result.image_data is not None:
        img = Image.fromarray((canvas_result.image_data[:, :, :3]).astype(np.uint8))
        img = img.convert("L")  # Convert to grayscale
        img = ImageOps.invert(img)  # Ensure black drawing on white background
        img = img.resize((28, 28), Image.LANCZOS)  # Resize to model input
        img_array = np.array(img) # Normalize
        img_array = img_array.reshape(1, 28, 28, 1)  # Reshape for model
        
        prediction = model.predict(img_array)
        predicted_class = np.argmax(prediction)
        
        st.image(img, caption="Processed Image", width=150)
        st.write(f"Predicted Class: {predicted_class}")
        st.bar_chart(prediction[0])

if st.button("Retry"):
    st.rerun()