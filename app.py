import streamlit as st
import yt_dlp
import os

# 1. Page Setup
st.set_page_config(page_title="SnapFetch AI", page_icon="🚀", layout="centered")

if "video_ready" not in st.session_state:
    st.session_state.video_ready = False
if "video_bytes" not in st.session_state:
    st.session_state.video_bytes = b""

st.markdown(
    """
    <style>
        :root {
            --slate-950: #020617;
            --slate-900: #0f172a;
            --charcoal-900: #111827;
            --charcoal-800: #1f2937;
            --text-main: #e2e8f0;
            --text-soft: #94a3b8;
        }
        .stApp {
            background: radial-gradient(circle at top, #131f38 0%, var(--slate-950) 56%, #01040c 100%);
            color: var(--text-main);
            font-family: "Inter", "Segoe UI", Roboto, Arial, sans-serif;
        }
        .main .block-container {
            max-width: 520px;
            padding-top: 2.1rem;
            padding-bottom: 2.3rem;
        }
        .header-wrap {
            text-align: center;
            margin-bottom: 1rem;
        }
        .header-icon {
            font-size: 3.2rem;
            line-height: 1;
            margin-bottom: 0.45rem;
            filter: drop-shadow(0 8px 22px rgba(99, 102, 241, 0.34));
        }
        .header-title {
            font-size: 2.1rem;
            font-weight: 700;
            color: #f8fafc;
            margin: 0;
            letter-spacing: 0.15px;
        }
        .header-subtitle {
            color: var(--text-soft);
            margin-top: 0.45rem;
            margin-bottom: 1.35rem;
        }
        .glass-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.04));
            border: 1px solid rgba(148, 163, 184, 0.2);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border-radius: 20px;
            padding: 1.15rem;
            box-shadow: 0 12px 35px rgba(2, 6, 23, 0.45);
            margin-bottom: 1rem;
        }
        .stTextInput > label {
            color: #cbd5e1;
            font-weight: 500;
        }
        .stTextInput > div > div > input {
            background-color: rgba(15, 23, 42, 0.75);
            color: #e2e8f0;
            border: 1px solid rgba(100, 116, 139, 0.45);
            border-radius: 14px;
            min-height: 48px;
        }
        div.stButton > button {
            background: linear-gradient(120deg, #4f46e5 0%, #7c3aed 100%);
            border-radius: 14px;
            color: white;
            font-weight: 600;
            padding: 0.78rem;
        }
        div.stDownloadButton > button {
            background: linear-gradient(120deg, #10b981 0%, #0ea5e9 100%);
            border-radius: 14px;
            color: white;
            font-weight: 600;
            padding: 0.78rem;
        }
        .how-to-card {
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 16px;
            padding: 1rem;
            margin-top: 0.85rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="header-wrap">
        <div class="header-icon">✦</div>
        <p class="header-title">SnapFetch AI</p>
        <p class="header-subtitle">High-speed media capture with a premium one-tap flow.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    url = st.text_input("Media URL", placeholder="Paste your link to unlock media...")
    fetch_clicked = st.button("Unlock Media", use_container_width=True)

    st.download_button(
        label="Download MP4",
        data=st.session_state.video_bytes,
        file_name="video.mp4",
        mime="video/mp4",
        disabled=not st.session_state.video_ready,
        use_container_width=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

if fetch_clicked:
    if not url:
        st.toast("Paste a media URL to continue.", icon="⚠️")
    else:
        temp_file = "downloaded_content.mp4"
        st.session_state.video_ready = False
        st.session_state.video_bytes = b""

        with st.status("Unlocking media...", expanded=True) as status:
            try:
                # Cleanup old files
                if os.path.exists(temp_file):
                    os.remove(temp_file)

                status.write("Configuring AI Fetcher...")
                ydl_opts = {
                    "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                    "merge_output_format": "mp4",
                    "outtmpl": temp_file,
                    "quiet": True,
                    "no_warnings": True,
                    "cookiefile": "cookies.txt",
                    "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
                    "referer": "https://www.youtube.com/",
                    "extractor_args": {
                        "youtube": {
                            "player_client": ["mweb"],
                        }
                    }
                }

                status.write("Bypassing security protocols...")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                if os.path.exists(temp_file):
                    status.write("Finalizing high-speed transfer...")
                    with open(temp_file, "rb") as f:
                        st.session_state.video_bytes = f.read()
                    st.session_state.video_ready = True
                    status.update(label="Media Unlocked Successfully!", state="complete")
                    st.toast("Tap the green button to save.", icon="✅")
                else:
                    status.update(label="Media not found.", state="error")
            except Exception as e:
                status.update(label="Unlock Failed", state="error")
                st.error(f"Reason: {str(e)}")
    else:
        temp_file = "downloaded_content.mp4"
        st.session_state.video_ready = False
        st.session_state.video_bytes = b""

        with st.status("Unlocking media...", expanded=True) as status:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)

                ydl_opts = {
                    "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                    "merge_output_format": "mp4",
                    "outtmpl": temp_file,
                    "quiet": True,
                    "no_warnings": True,
                    "cookiefile": "cookies.txt",
                    "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
                    "referer": "https://www.youtube.com/",
                    "extractor_args": {
                        "youtube": {
                            "player_client": ["mweb"],
                            "po_token": ["web+MnS8O..."],
                        }
                    }
                }

                status.write("Fetching stream...")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                if os.path.exists(temp_file):
                    with open(temp_file, "rb") as f:
                        st.session_state.video_bytes = f.read()
                    st.session_state.video_ready = True
                    status.update(label="Media unlocked!", state="complete")
                    st.toast("Ready to download.", icon="✅")
                else:
                    status.update(label="File not found.", state="error")
            except Exception as e:
                status.update(label="Unlock failed", state="error")
                st.error(f"Error: {str(e)}")

st.markdown(
    """
    <div class="how-to-card">
        <p style="color:white; font-weight:bold;">How to use</p>
        <p style="color:#cbd5e1;">🔗 Paste a media URL.</p>
        <p style="color:#cbd5e1;">🟣 Tap Unlock Media.</p>
        <p style="color:#cbd5e1;">🌊 Tap Download MP4.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
