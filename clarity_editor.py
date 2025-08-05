
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import zipfile
import os

st.set_page_config(page_title="Clarity Editor Pro", layout="centered")

st.markdown("""
<style>
    .main {
        background-color: #121212;
        color: white;
    }
    .stApp {
        font-family: 'Poppins', sans-serif;
    }
    .block-container {
        padding: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.image("https://raw.githubusercontent.com/openai/clarity-brand-assets/main/clarity_logo_banner.png", width=280)
st.markdown("### ✨ Clarity Editor Pro")
st.markdown("**Create with Clarity. Share with Purpose.**")
st.markdown("---")

avatar = st.file_uploader("📤 Upload an image (JPG/PNG)", type=["jpg", "png"])

# Font selection and styling
font_files = {
    "Poppins": "fonts/Poppins-Regular.ttf",
    "Montserrat": "fonts/Montserrat-Regular.ttf",
    "Playfair Display": "fonts/PlayfairDisplay-Regular.ttf",
    "Sora": "fonts/Sora-Regular.ttf",
    "Inter": "fonts/Inter-Regular.ttf"
}

font_choice = st.selectbox("🔠 Choose a font style", list(font_files.keys()))
font_size = st.slider("🔧 Font size", 24, 60, 36)
text_color = st.color_picker("🎨 Text color", "#FFFFFF")
bg_color = st.color_picker("🎨 Background panel color", "#000000")

quote1 = st.text_input("💬 Quote 1 (top)", "")
quote2 = st.text_input("💬 Quote 2 (middle)", "")
quote3 = st.text_input("💬 Quote 3 (bottom)", "")

if avatar and (quote1 or quote2 or quote3):
    image = Image.open(avatar).convert("RGBA")
    draw = ImageDraw.Draw(image)

    try:
        font_path = font_files[font_choice]
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()

    # Draw background panel
    draw.rectangle([0, image.height - 150, image.width, image.height], fill=bg_color)

    # Draw quotes
    quotes = [quote1, quote2, quote3]
    spacing = font_size + 10
    y_start = image.height - 140
    for q in quotes:
        if q:
            draw.text((30, y_start), q, fill=text_color, font=font)
            y_start += spacing

    st.image(image, caption="🔍 Polished Preview", use_container_width=True)

    # PNG Output
    output = io.BytesIO()
    image.save(output, format="PNG")
    st.download_button("📥 Download Image", output.getvalue(), file_name="clarity_pro_image.png")

    # ZIP Output
    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "a", zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr("quotes.txt", "\n".join([q for q in quotes if q]))
        output.seek(0)
        zipf.writestr("clarity_pro_image.png", output.read())
    zip_buf.seek(0)
    st.download_button("📦 Download Pro Kit (.zip)", zip_buf, file_name="clarity_pro_kit.zip")
else:
    st.info("Please upload an image and enter at least one quote.")
