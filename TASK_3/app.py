
import streamlit as st
from PIL import Image
from transformers import pipeline

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Image Captioning AI",
    page_icon="🖼️",
    layout="centered"
)

# ---------------- CUSTOM DESIGN ----------------
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
    border: none;
    padding: 12px;
    font-weight: bold;
}
.stButton > button:hover {
    background: #00b894;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("🖼️ Image Captioning AI")
st.write("Upload an image and let AI describe it!")
st.caption("Powered by Python, Streamlit and BLIP AI")

st.divider()

# ---------------- LOAD MODEL ----------------
@st.cache_resource(show_spinner=False)
def load_model():
    return pipeline(
        "image-to-text",
        model="Salesforce/blip-image-captioning-base"
    )

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
            with st.spinner(
                "AI is analyzing your image..."
            ):
                model = load_model()
                result = model(
                    image,
                    max_new_tokens=50
                )
                caption = result[0]["generated_text"]

            st.success("Caption Generated Successfully!")

            st.subheader("📝 Generated Caption")
            st.markdown(
                f"**{caption[:1].upper() + caption[1:]}**"
            )

            st.download_button(
                label="📥 Download Caption",
                data=caption,
                file_name="image_caption.txt",
                mime="text/plain"
            )

    except Exception as e:
        st.error("Unable to generate caption.")
        st.caption(f"Error details: {e}")

else:
    st.info("👆 Upload an image to get started.")

# ---------------- FOOTER ----------------
st.divider()
st.caption("AI/ML Project | Image Captioning AI ❤️")

