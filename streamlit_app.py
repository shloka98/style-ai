import streamlit as st
import openai
import os
import tempfile
from PIL import Image

openai.api_key = os.environ.get("OPENAI_API_KEY")

st.set_page_config(page_title="AI Wardrobe Assistant", layout="wide")
st.title("👗 AI Wardrobe Assistant")
st.markdown("Upload your wardrobe and let GPT-4 style you for any occasion ✨")

with st.form("style_form"):
    instagram = st.text_input("Instagram handle")
    pinterest = st.text_input("Pinterest URL")
    occasion = st.text_input("Occasions (e.g., work, weddings, casual)")
    dislikes = st.text_area("Dislikes / styles to avoid")
    budget = st.text_input("Shopping budget (optional)")
    location = st.text_input("Location (to tailor links)")
    uploaded_files = st.file_uploader("Upload wardrobe images", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
    submitted = st.form_submit_button("Generate Style Guide")

if submitted:
    if not uploaded_files:
        st.error("Please upload at least one wardrobe image.")
    else:
        with st.spinner("Generating your personalized lookbook and shopping guide..."):
            saved_paths = []
            for file in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=file.name[-4:]) as tmp:
                    tmp.write(file.read())
                    saved_paths.append(tmp.name)

            prompt = (
                "You are a fashion stylist AI. Based on the user's wardrobe and preferences, generate:\n"
                "1. Complete outfits for each occasion type.\n"
                "2. Shopping recommendations for missing basics or pieces that would complement existing wardrobe items.\n\n"
                f"Instagram: {instagram}\n"
                f"Pinterest: {pinterest}\n"
                f"Occasion Types: {occasion}\n"
                f"Dislikes: {dislikes}\n"
                f"Budget: {budget}\n"
                f"Location: {location}\n\n"
                "Wardrobe:\n"
            )
            for i, path in enumerate(saved_paths):
                prompt += f"Item {i+1}: [Image not shown]\n"

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a fashion stylist."},
                    {"role": "user", "content": prompt}
                ]
            )

            output = response['choices'][0]['message']['content']

            st.subheader("🧾 AI Styling Recommendations")
            st.markdown(output)

            st.subheader("👚 Your Uploaded Wardrobe")
            cols = st.columns(5)
            for i, path in enumerate(saved_paths):
                with cols[i % 5]:
                    st.image(path, use_column_width=True)

            for path in saved_paths:
                os.remove(path)
