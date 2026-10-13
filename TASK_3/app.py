
import streamlit as st
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Image Captioning AI",
    page_icon="🖼️",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101827, #263b5e);
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
.stButton > button {
    width: 100%;
    background: #00d4aa;
    color: #101827;
    border-radius: 12px;
    padding: 12px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("🖼️ Image Captioning AI")
st.write("Upload an image and let AI describe it!")
st.caption("Powered by Python, Streamlit and BLIP AI")
st.divider()

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    model_name = "Salesforce/blip-image-captioning-base"

    processor = BlipProcessor.from_pretrained(model_name)
    model = BlipForConditionalGeneration.from_pretrained(model_name)

    model.eval()
    return processor, model

# ---------------- IMAGE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "📤 Choose an image",
    type=["jpg", "jpeg", "png", "webp"]
)

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file).convert("RGB")

        st.image(
            image,
            caption="Uploaded Image",
            use_container_width=True
        )

        if st.button("✨ Generate Caption"):
            with st.spinner("AI is analyzing your image..."):
                processor, model = load_model()

                inputs = processor(
                    images=image,
                    return_tensors="pt"
                )

                with torch.no_grad():
                    output = model.generate(
                        **inputs,
                        max_new_tokens=50
                    )

                caption = processor.decode(
                    output[0],
                    skip_special_tokens=True
                )

            st.success("Caption generated successfully!")
            st.subheader("📝 Generated Caption")
            st.write(caption.capitalize())

            st.download_button(
                "📥 Download Caption",
                data=caption,
                file_name="image_caption.txt",
                mime="text/plain"
            )

    except Exception as e:
        st.error("Unable to generate caption.")
        st.exception(e)

else:
    st.info("👆 Upload an image to get started.")

st.divider()
st.caption("AI/ML Project | Image Captioning AI ❤️")
