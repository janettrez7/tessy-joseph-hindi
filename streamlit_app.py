import streamlit as st
import os
import json
from pathlib import Path

CATEGORIES = ["Class 8", "Class 10"]
BASE_DIR = Path("uploads")
YOUTUBE_FILE = Path("youtube_links.json")

for cat in CATEGORIES:
    (BASE_DIR / cat).mkdir(parents=True, exist_ok=True)
if not YOUTUBE_FILE.exists():
    YOUTUBE_FILE.write_text("[]")

with open(YOUTUBE_FILE, "r") as f:
    youtube_links = json.load(f)

st.set_page_config(page_title="Teaching Portal", layout="wide")
st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>📚 Tessy Joseph HST (Hindi) Teaching Portal</h1>", unsafe_allow_html=True)

st.subheader("📤 Upload Teaching Materials")
selected_category = st.selectbox("Select Class", CATEGORIES)
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

st.subheader("🎥 Add YouTube Videos")
with st.form("add_youtube_form"):
    yt_url = st.text_input("Enter YouTube URL")
    submit_yt = st.form_submit_button("Add Video")
    if submit_yt and yt_url:
        youtube_links.append(yt_url)
        with open(YOUTUBE_FILE, "w") as f:
            json.dump(youtube_links, f)
        st.success("YouTube video added!")
        st.experimental_rerun()

if youtube_links:
    st.subheader("📺 Stored YouTube Videos")
    for idx, link in enumerate(youtube_links):
        col1, col2 = st.columns([6, 1])
        with col1:
            st.video(link)
        with col2:
            if st.button("🗑️ Delete", key=f"yt_{idx}"):
                youtube_links.pop(idx)
                with open(YOUTUBE_FILE, "w") as f:
                    json.dump(youtube_links, f)
                st.warning("Video removed")
                st.experimental_rerun()

st.subheader("📁 View Teaching Material")

card_style = """
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 15px;
    margin: 10px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    text-align: center;
"""

for category in CATEGORIES:
    files = os.listdir(BASE_DIR / category)
    if files:
        st.markdown(f"<h4 style='margin-top:40px;'>📂 {category} ({len(files)} files)</h4>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, file in enumerate(files):
            file_path = BASE_DIR / category / file
            with cols[i % 3]:
                st.markdown(f"<div style='{card_style}'>", unsafe_allow_html=True)
                if file.endswith((".png", ".jpg", ".jpeg")):
                    st.image(str(file_path), width=250)
                elif file.endswith(".mp4"):
                    st.video(str(file_path))
                elif file.endswith(".pdf"):
                    st.markdown(f"[📄 View PDF: {file}](/{file_path})", unsafe_allow_html=True)
                else:
                    st.text(file)

                st.caption(file)
                if st.button("🗑️ Delete", key=f"del_{category}_{file}"):
                    os.remove(file_path)
                    st.warning(f"Deleted {file}")
                    st.experimental_rerun()
                st.markdown("</div>", unsafe_allow_html=True)
