import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import io

st.set_page_config(page_title="🎨 Color Recognition", layout="centered")
st.title("🎨 Color Recognition App")

uploaded_file = st.file_uploader("📤 Upload an Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="🖼️ Uploaded Image", use_container_width=True)

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_bytes = img_byte_arr.getvalue()
    image_for_canvas = Image.open(io.BytesIO(img_bytes))

    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0.0)",
        stroke_width=1,
        background_image=image_for_canvas,
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="transform",
        key="canvas"
    )

    if canvas_result.json_data and canvas_result.json_data["objects"]:
        last_obj = canvas_result.json_data["objects"][-1]
        x = int(last_obj["left"])
        y = int(last_obj["top"])

        x = min(max(x, 0), image.width - 1)
        y = min(max(y, 0), image.height - 1)

        rgb = np.array(image)[y, x]
        hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb)

        st.markdown(f"📍 **Position:** `{x}, {y}`")
        st.markdown(f"🎨 **RGB:** `{tuple(rgb)}`")
        st.markdown(f"🟢 **Hex:** `{hex_color}`")
        st.color_picker("Color Preview", hex_color, label_visibility="collapsed", disabled=True)

else:
    st.info("📥 Upload an image to detect colors.")
