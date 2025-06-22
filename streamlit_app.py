import streamlit as st
import os
import json
from pathlib import Path

CATEGORIES = ["Class 8 C", "Class 8 D", "Class 8 E", "Class 10 C"]
BASE_DIR = Path("uploads")
YOUTUBE_FILE = Path("youtube_links.json")

for cat in CATEGORIES:
    (BASE_DIR / cat).mkdir(parents=True, exist_ok=True)
if not YOUTUBE_FILE.exists():
    YOUTUBE_FILE.write_text("[]")

with open(YOUTUBE_FILE, "r") as f:
    youtube_links = json.load(f)

st.set_page_config(page_title="Teaching Portal", layout="wide")
st.title("📚 Tessy Joseph HST (Hindi) Teaching Portal")

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
    if submit_yt:
        if yt_url.startswith("http"):
            youtube_links.append(yt_url)
            with open(YOUTUBE_FILE, "w") as f:
                json.dump(youtube_links, f)
            st.success("YouTube video added!")
            st.experimental_rerun()
        else:
            st.error("Please enter a valid YouTube URL starting with http or https.")

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
                        st.warning("Deleted")
                        st.experimental_rerun()
