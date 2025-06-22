import streamlit as st
import os
from pathlib import Path

# Define categories (you can customize this)
CATEGORIES = ["General", "English", "Maths", "Science"]

# Create folders for each category
BASE_DIR = Path("uploads")
for cat in CATEGORIES:
    (BASE_DIR / cat).mkdir(parents=True, exist_ok=True)

st.title("📚 Teaching Material Portal")

# --- Upload Section ---
st.subheader("📤 Upload Teaching Materials")
selected_category = st.selectbox("Select Category", CATEGORIES)
uploaded_files = st.file_uploader(
    "Choose files to upload",
    accept_multiple_files=True,
    type=["png", "jpg", "jpeg", "mp4", "pdf"]
)

if uploaded_files:
    for file in uploaded_files:
        save_path = BASE_DIR / selected_category / file.name
        with open(save_path, "wb") as f:
            f.write(file.getbuffer())
        st.success(f"Uploaded to {selected_category}: {file.name}")

# --- Display Section ---
st.subheader("📁 View and Manage Files")

for category in CATEGORIES:
    files = os.listdir(BASE_DIR / category)
    if files:
        with st.expander(f"📂 {category} ({len(files)} files)"):
            for file in files:
                file_path = BASE_DIR / category / file
                col1, col2 = st.columns([6, 1])

                with col1:
                    if file.endswith((".png", ".jpg", ".jpeg")):
                        st.image(str(file_path), width=300)
                    elif file.endswith(".mp4"):
                        st.video(str(file_path))
                    elif file.endswith(".pdf"):
                        st.markdown(f"[📄 View PDF: {file}](/{file_path})", unsafe_allow_html=True)
                    else:
                        st.text(file)

                with col2:
                    if st.button("🗑️ Delete", key=f"del_{category}_{file}"):
                        os.remove(file_path)
                        st.warning(f"Deleted: {file}")
                        st.experimental_rerun()
