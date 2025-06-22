import streamlit as st
import os
from pathlib import Path

UPLOAD_DIR = "uploads"
Path(UPLOAD_DIR).mkdir(exist_ok=True)

st.title("📚 Teaching Material Portal")

uploaded_files = st.file_uploader(
    "Upload teaching files (PDFs, images, videos)", 
    accept_multiple_files=True,
    type=['png', 'jpg', 'jpeg', 'mp4', 'pdf']
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Uploaded {uploaded_file.name}")

st.header("📂 Uploaded Materials")

for file_name in os.listdir(UPLOAD_DIR):
    file_path = os.path.join(UPLOAD_DIR, file_name)
    if file_name.endswith((".png", ".jpg", ".jpeg")):
        st.image(file_path, caption=file_name)
    elif file_name.endswith(".mp4"):
        st.video(file_path)
    elif file_name.endswith(".pdf"):
        st.markdown(f"[📄 View PDF: {file_name}](/{file_path})", unsafe_allow_html=True)
