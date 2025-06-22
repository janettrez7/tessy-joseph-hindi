import streamlit as st
import os
import json
import zipfile
from pathlib import Path
from urllib.parse import quote

# -----------------------
# USER CONFIG
# -----------------------
USERS = {
    "teacher1": "pass123",
    "tessy": "hindi2024"
}

CATEGORIES = ["Class 8 C", "Class 8 D", "Class 8 E", "Class 10 C"]
BASE_DIR = Path("uploads")
YOUTUBE_FILE = Path("youtube_links.json")

# -----------------------
# SETUP
# -----------------------
for cat in CATEGORIES:
    (BASE_DIR / cat).mkdir(parents=True, exist_ok=True)

if not YOUTUBE_FILE.exists():
    YOUTUBE_FILE.write_text("[]")

with open(YOUTUBE_FILE, "r") as f:
    youtube_links = json.load(f)

st.set_page_config(page_title="Teaching Portal", layout="centered")

# -----------------------
# LOGIN
# -----------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Welcome Tessy, please login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials. Try again.")
    st.stop()

# -----------------------
# SIDEBAR NAVIGATION (Always Open)
# -----------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/female-teacher.png", width=80)
    st.title("👩‍🏫 Tessy Joseph")
    st.caption("HST - Hindi Teacher OLCGHS Palluruthy")
    page = st.radio("Navigate", ["Upload Materials", "YouTube Gallery", "All Files"])

# -----------------------
# PAGE 1: UPLOAD MATERIALS
# -----------------------
if page == "Upload Materials":
    st.title("📤 Upload Teaching Materials")
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

# -----------------------
# PAGE 2: YOUTUBE GALLERY
# -----------------------
elif page == "YouTube Gallery":
    st.title("🎥 YouTube Video Gallery")

    with st.form("add_youtube_form"):
        yt_url = st.text_input("Enter YouTube URL")
        submit_yt = st.form_submit_button("Add Video")
        if submit_yt:
            if yt_url.startswith("http"):
                youtube_links.append(yt_url)
                with open(YOUTUBE_FILE, "w") as f:
                    json.dump(youtube_links, f)
                st.success("YouTube video added!")
            else:
                st.error("Please enter a valid YouTube URL starting with http or https.")

    if youtube_links:
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
                    st.rerun()

# -----------------------
# PAGE 3: VIEW FILES
# -----------------------
elif page == "All Files":
    st.title("📁 View Teaching Materials")

    for category in CATEGORIES:
        files = os.listdir(BASE_DIR / category)
        if files:
            with st.expander(f"📂 {category} ({len(files)} files)"):

                zip_filename = f"{category.replace(' ', '_')}.zip"
                zip_path = BASE_DIR / zip_filename
                with zipfile.ZipFile(zip_path, "w") as zipf:
                    for file in files:
                        file_path = BASE_DIR / category / file
                        zipf.write(file_path, arcname=file)
                with open(zip_path, "rb") as zf:
                    st.download_button(
                        label=f"⬇️ Download all files from {category}",
                        data=zf,
                        file_name=zip_filename,
                        mime="application/zip"
                    )

                for file in files:
                    file_path = BASE_DIR / category / file
                    col1, col2 = st.columns([6, 1])
                    with col1:
                        if file.endswith((".png", ".jpg", ".jpeg")):
                            st.image(str(file_path), width=300)
                        elif file.endswith(".mp4"):
                            st.video(str(file_path))
                        elif file.endswith(".pdf"):
                            encoded_path = quote(str(file_path))
                            st.markdown(
                                f'<a href="{encoded_path}" target="_blank">📄 View PDF: {file}</a>',
                                unsafe_allow_html=True
                            )
                        else:
                            st.text(file)
                    with col2:
                        if st.button("🗑️ Delete", key=f"del_{category}_{file}"):
                            os.remove(file_path)
                            st.warning("Deleted")
                            st.rerun()
