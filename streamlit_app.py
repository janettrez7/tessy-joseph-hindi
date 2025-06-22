import streamlit as st
import os
import json
import zipfile
from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse, parse_qs

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

st.set_page_config(page_title="Teaching Portal", layout="wide")

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
# HEADER & THEME TOGGLE
# -----------------------

st.markdown("""
    <div style="display:flex; align-items:center; justify-content:space-between;
                background-color:#263238; padding:10px 20px; border-radius:8px; color:white;">
        <div>
            <h2 style="margin:0;">📚 Tessy Joseph</h2>
            <p style="margin:0;">HST - Hindi Teacher</p>
        </div>
        <div>
            <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="50" style="border-radius:50%;">
        </div>
    </div>
""", unsafe_allow_html=True)

# Theme toggle
mode = st.sidebar.radio("🌓 Theme", ["🌞 Light", "🌙 Dark"])
if mode == "🌙 Dark":
    st.markdown("""
        <style>
        body, .stApp { background-color: #111 !important; color: white !important; }
        </style>
    """, unsafe_allow_html=True)

# -----------------------
# SIDEBAR NAVIGATION
# -----------------------

page = st.sidebar.radio("📂 Navigation", ["Upload", "YouTube Videos", "View Files"])

# -----------------------
# UPLOAD SECTION
# -----------------------

if page == "Upload":
    st.subheader("📤 Upload Teaching Materials")
    selected_category = st.selectbox("Select Class", CATEGORIES)
    uploaded_files = st.file_uploader(
        "Choose files to upload", accept_multiple_files=True, type=["png", "jpg", "jpeg", "mp4", "pdf"]
    )

    if uploaded_files:
        for file in uploaded_files:
            save_path = BASE_DIR / selected_category / file.name
            with open(save_path, "wb") as f:
                f.write(file.getbuffer())
            st.success(f"Uploaded to {selected_category}: {file.name}")

# -----------------------
# YOUTUBE SECTION
# -----------------------

def get_thumbnail(url):
    video_id = parse_qs(urlparse(url).query).get("v")
    if video_id:
        return f"https://img.youtube.com/vi/{video_id[0]}/0.jpg"
    return ""

if page == "YouTube Videos":
    st.subheader("🎥 Add YouTube Videos")
    if "yt_added" not in st.session_state:
        st.session_state["yt_added"] = False

    with st.form("add_youtube_form"):
        yt_url = st.text_input("Enter YouTube URL")
        submit_yt = st.form_submit_button("Add Video")
        if submit_yt:
            if yt_url.startswith("http"):
                youtube_links.append(yt_url)
                with open(YOUTUBE_FILE, "w") as f:
                    json.dump(youtube_links, f)
                st.session_state["yt_added"] = True
            else:
                st.error("Please enter a valid YouTube URL starting with http or https.")

    if st.session_state["yt_added"]:
        st.success("YouTube video added!")
        st.session_state["yt_added"] = False

    if youtube_links:
        st.subheader("📺 Stored YouTube Videos")
        for idx, link in enumerate(youtube_links):
            col1, col2 = st.columns([6, 1])
            with col1:
                st.image(get_thumbnail(link), caption="YouTube Preview", width=300)
                st.markdown(f"[▶️ Watch Video]({link})", unsafe_allow_html=True)
            with col2:
                if st.button("🗑️ Delete", key=f"yt_{idx}"):
                    youtube_links.pop(idx)
                    with open(YOUTUBE_FILE, "w") as f:
                        json.dump(youtube_links, f)
                    st.warning("Video removed")
                    st.rerun()

# -----------------------
# VIEW FILES SECTION + BULK DOWNLOAD
# -----------------------

if page == "View Files":
    st.subheader("📁 View Teaching Material")
    for category in CATEGORIES:
        files = os.listdir(BASE_DIR / category)
        if files:
            with st.expander(f"📂 {category} ({len(files)} files)"):
                with BytesIO() as zip_buffer:
                    with zipfile.ZipFile(zip_buffer, "w") as zipf:
                        for file in files:
                            file_path = BASE_DIR / category / file
                            zipf.write(file_path, arcname=file)
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
                                    st.rerun()
                    zip_buffer.seek(0)
                    st.download_button(
                        label=f"⬇️ Download all files from {category}",
                        data=zip_buffer,
                        file_name=f"{category.replace(' ', '_')}_files.zip",
                        mime="application/zip"
                    )
