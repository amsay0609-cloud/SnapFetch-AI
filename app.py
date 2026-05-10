import streamlit as st
import yt_dlp
import os

# 1. Page Setup
st.set_page_config(page_title="SnapFetch AI", page_icon="🚀", layout="centered")

if "video_ready" not in st.session_state:
    st.session_state.video_ready = False
if "video_bytes" not in st.session_state:
    st.session_state.video_bytes = b""

# CSS and Header (Keeping your premium look)
st.markdown("""
    <style>
        :root { --slate-950: #020617; --text-main: #e2e8f0; }
        .stApp { background: radial-gradient(circle at top, #131f38 0%, var(--slate-950) 56%); color: var(--text-main); }
        .glass-card { background: rgba(255, 255, 255, 0.05); border-radius: 20px; padding: 1.5rem; border: 1px solid rgba(255,255,255,0.1); }
        div.stButton > button { background: linear-gradient(120deg, #4f46e5 0%, #7c3aed 100%); border-radius: 14px; color: white; width: 100%; }
        div.stDownloadButton > button { background: linear-gradient(120deg, #10b981 0%, #0ea5e9 100%); border-radius: 14px; color: white; width: 100%; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div style="text-align:center;"><h1>✦ SnapFetch AI</h1><p>Premium High-Speed Media Capture</p></div>', unsafe_allow_html=True)

# 2. UI Elements
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    # Yahan user apna link daalega
    url = st.text_input("Media URL", placeholder="Paste YouTube/Pinterest link here...")
    fetch_clicked = st.button("Unlock Media")

    if st.session_state.video_ready:
        st.download_button(
            label="Download MP4",
            data=st.session_state.video_bytes,
            file_name="SnapFetch_Video.mp4",
            mime="video/mp4"
        )
    st.markdown('</div>', unsafe_allow_html=True)

# 3. Logic - Jab button click ho
if fetch_clicked:
    if not url:
        st.toast("Please paste a URL first!", icon="⚠️")
    else:
        temp_file = "downloaded_video.mp4"
        
        with st.status("Processing Media...", expanded=True) as status:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)

                # Aapke run_test.py wali settings yahan hain:
                ydl_opts = {
                    # Yeh line user ke 'url' se best video aur audio uthayegi
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'merge_output_format': 'mp4',
                    'outtmpl': 'downloaded_video.%(ext)s',
                    'cookiefile': 'cookies.txt',
                    'quiet': False,
                    'nocheckcertificate': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
                }

                status.write("Fetching best quality streams...")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Yahan fix link ki jagah 'url' variable use ho raha hai
                    ydl.download([url])

                if os.path.exists(temp_file):
                    status.write("Preparing for download...")
                    with open(temp_file, "rb") as f:
                        st.session_state.video_bytes = f.read()
                    st.session_state.video_ready = True
                    status.update(label="Media Ready!", state="complete")
                    st.rerun() # UI refresh karne ke liye taaki download button dikhe
                else:
                    status.update(label="Media not found on server.", state="error")
                    
            except Exception as e:
                status.update(label="Failed to fetch media", state="error")
                st.error(f"Reason: {str(e)}")
