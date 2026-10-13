
import os
import csv
import uuid
import io

import streamlit as st
import torch
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration
)

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Self-Improving Image Caption AI",
    page_icon="🤖",
    layout="centered"
)

DATA_DIR = "feedback_images"
CSV_FILE = "feedback.csv"
MODEL_DIR = "improved_blip_model"
BASE_MODEL = "Salesforce/blip-image-captioning-base"

os.makedirs(DATA_DIR, exist_ok=True)

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

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
    border-radius: 10px;
    padding: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 Self-Improving Image Caption AI")
st.write("Generate captions, correct mistakes and fine-tune AI.")
st.caption(f"Running on: {DEVICE}")

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    model_path = (
        MODEL_DIR
        if os.path.isfile(os.path.join(MODEL_DIR, "config.json"))
        else BASE_MODEL
    )

    processor = BlipProcessor.from_pretrained(model_path)
    model = BlipForConditionalGeneration.from_pretrained(
        model_path
    )
    model.to(DEVICE)
    model.eval()

    return processor, model


# ---------------- TRAINING DATASET ----------------
class CaptionDataset(Dataset):
    def __init__(self, records):
        self.records = records

    def __len__(self):
        return len(self.records)

    def __getitem__(self, index):
        row = self.records[index]

        with Image.open(row["image_path"]) as img:
            image = img.convert("RGB").copy()

        caption = row["target_caption"].strip()
        return image, caption


def collate_batch(batch, processor):
    images, captions = zip(*batch)

    encoded = processor(
        images=list(images),
        text=list(captions),
        padding="max_length",
        truncation=True,
        max_length=40,
        return_tensors="pt"
    )

    labels = encoded["input_ids"].clone()
    labels[labels == processor.tokenizer.pad_token_id] = -100

    return {
        "pixel_values": encoded["pixel_values"],
        "input_ids": encoded["input_ids"],
        "attention_mask": encoded["attention_mask"],
        "labels": labels
    }


# ---------------- GENERATE CAPTION ----------------
uploaded = st.file_uploader(
    "📤 Upload an image",
    type=["jpg", "jpeg", "png", "webp"]
)

if uploaded:
    image = Image.open(uploaded).convert("RGB")
    st.image(image, caption="Your image", use_container_width=True)

    if st.button("✨ Generate Caption"):
        try:
            with st.spinner("Analyzing image..."):
                processor, model = load_model()
                inputs = processor(
                    images=image,
                    return_tensors="pt"
                ).to(DEVICE)

                model.eval()
                with torch.no_grad():
                    output = model.generate(
                        **inputs,
                        max_new_tokens=40
                    )

                caption = processor.decode(
                    output[0],
                    skip_special_tokens=True
                )

                st.session_state["caption"] = caption
                st.session_state["image_bytes"] = uploaded.getvalue()

        except Exception as e:
            st.error(f"Caption generation failed: {e}")

# ---------------- FEEDBACK ----------------
if "caption" in st.session_state:
    st.subheader("📝 AI Caption")
    st.info(st.session_state["caption"])

    feedback = st.radio(
        "Is the caption correct?",
        ["Correct", "Incorrect"],
        key="feedback_choice"
    )

    corrected = st.session_state["caption"]

    if feedback == "Incorrect":
        corrected = st.text_area(
            "Enter the correct image caption",
            placeholder="Describe what is actually visible in the image.",
            key="corrected_caption"
        )

    if st.button("💾 Save Feedback"):
        target = corrected.strip()

        if not target:
            st.warning("Please enter a correct caption.")
        else:
            try:
                image_id = uuid.uuid4().hex
                image_path = os.path.join(
                    DATA_DIR, f"{image_id}.jpg"
                )

                Image.open(
                    io.BytesIO(st.session_state["image_bytes"])
                ).convert("RGB").save(image_path, "JPEG")

                exists = os.path.exists(CSV_FILE)

                with open(
                    CSV_FILE, "a", newline="", encoding="utf-8"
                ) as file:
                    writer = csv.DictWriter(
                        file,
                        fieldnames=[
                            "image_path",
                            "generated_caption",
                            "feedback",
                            "target_caption"
                        ]
                    )

                    if not exists:
                        writer.writeheader()

                    writer.writerow({
                        "image_path": image_path,
                        "generated_caption": st.session_state["caption"],
                        "feedback": feedback,
                        "target_caption": target
                    })

                st.success("Feedback saved as training data!")

                del st.session_state["caption"]
                del st.session_state["image_bytes"]

            except Exception as e:
                st.error(f"Could not save feedback: {e}")

# ---------------- TRAIN MODEL ----------------
st.divider()
st.subheader("🧠 Improve AI with Feedback")

records = []

if os.path.exists(CSV_FILE):
    try:
        with open(CSV_FILE, newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                if (
                    row.get("target_caption", "").strip()
                    and os.path.isfile(row.get("image_path", ""))
                ):
                    records.append(row)
    except Exception as e:
        st.error(f"Could not read training data: {e}")

st.write(f"Saved training examples: **{len(records)}**")
st.caption(
    "For useful fine-tuning, collect many diverse, accurate "
    "image-caption pairs. A few examples are only a small start."
)

epochs = st.select_slider(
    "Training epochs",
    options=[1, 2, 3],
    value=1
)

if st.button("🚀 Improve AI"):
    if len(records) < 2:
        st.warning("Save at least 2 image-caption examples first.")
    else:
        try:
            processor, model = load_model()
            model.train()

            dataset = CaptionDataset(records)
            loader = DataLoader(
                dataset,
                batch_size=1,
                shuffle=True,
                collate_fn=lambda batch: collate_batch(
                    batch, processor
                )
            )

            optimizer = torch.optim.AdamW(
                model.parameters(),
                lr=2e-5
            )

            progress = st.progress(0)
            status = st.empty()
            total_steps = epochs * len(loader)
            step = 0
            last_loss = 0.0

            for epoch in range(epochs):
                for batch in loader:
                    batch = {
                        key: value.to(DEVICE)
                        for key, value in batch.items()
                    }

                    optimizer.zero_grad()

                    outputs = model(**batch)
                    loss = outputs.loss
                    loss.backward()

                    torch.nn.utils.clip_grad_norm_(
                        model.parameters(), 1.0
                    )
                    optimizer.step()

                    last_loss = loss.item()
                    step += 1
                    progress.progress(step / total_steps)
                    status.write(
                        f"Epoch {epoch + 1}/{epochs} | "
                        f"Step {step}/{total_steps} | "
                        f"Loss: {last_loss:.4f}"
                    )

            model.eval()
            os.makedirs(MODEL_DIR, exist_ok=True)
            model.save_pretrained(MODEL_DIR)
            processor.save_pretrained(MODEL_DIR)

            st.cache_resource.clear()

            st.success(
                "Fine-tuning completed! The updated model was saved."
            )
            st.write(f"Final training loss: {last_loss:.4f}")
            st.info(
                "Generate a new caption to test the saved model. "
                "Lower training loss alone does not guarantee "
                "better captions on unseen images."
            )

        except Exception as e:
            st.error(f"Training failed: {e}")
            st.info(
                "Try fewer examples or epochs, check available "
                "RAM, and ensure the model downloaded correctly."
            )

