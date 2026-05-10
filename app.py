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
        .stTextInput > div > div > input:focus {
            border: 1px solid rgba(99, 102, 241, 0.95);
            box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25);
        }
        div.stButton, div.stDownloadButton {
            width: 100%;
        }
        div.stButton > button,
        div.stDownloadButton > button {
            width: 100%;
            border-radius: 14px;
            border: 1px solid rgba(148, 163, 184, 0.16);
            font-weight: 600;
            padding: 0.78rem 0.95rem;
            color: #ffffff;
            transition: all 0.2s ease-in-out;
        }
        div.stButton > button {
            background: linear-gradient(120deg, #4f46e5 0%, #7c3aed 100%);
            box-shadow: 0 8px 24px rgba(79, 70, 229, 0.32);
        }
        div.stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 26px rgba(99, 102, 241, 0.38);
        }
        div.stDownloadButton > button {
            background: linear-gradient(120deg, #10b981 0%, #0ea5e9 100%);
            box-shadow: 0 0 0 rgba(16, 185, 129, 0.15), 0 10px 26px rgba(14, 165, 233, 0.26);
        }
        div.stDownloadButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 0 18px rgba(16, 185, 129, 0.3), 0 12px 28px rgba(14, 165, 233, 0.33);
        }
        div.stDownloadButton > button:disabled {
            opacity: 0.55;
            cursor: not-allowed;
            box-shadow: none;
        }
        .how-to-card {
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 16px;
            padding: 1rem;
            margin-top: 0.85rem;
        }
        .how-to-title {
            font-size: 1.06rem;
            font-weight: 650;
            color: #f8fafc;
            margin-bottom: 0.52rem;
        }
        .how-to-item {
            color: #cbd5e1;
            margin: 0.3rem 0;
        }
        @media (max-width: 640px) {
            .main .block-container {
                max-width: 100%;
                padding-left: 0.95rem;
                padding-right: 0.95rem;
                padding-top: 1.25rem;
            }
            .glass-card, .how-to-card {
                border-radius: 16px;
                padding: 0.95rem;
            }
            .header-title {
                font-size: 1.7rem;
            }
            .header-icon {
                font-size: 2.8rem;
            }
            div.stButton > button,
            div.stDownloadButton > button {
                min-height: 48px;
            }
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

    # 2. Input
    url = st.text_input("Media URL", placeholder="Paste your link to unlock media...")

    # 3. Processing
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
                status.write("Validating your link")

                if os.path.exists(temp_file):
                    os.remove(temp_file)

                ydl_opts = {
                    "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                    "merge_output_format": "mp4",
                    "outtmpl": temp_file,
                    "quiet": True,
                    "no_warnings": True,
                    "cookiefile": "cookies.txt",  # ADD THIS LINE
                }

                status.write("Fetching highest quality stream")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                if os.path.exists(temp_file):
                    with open(temp_file, "rb") as video_file:
                        st.session_state.video_bytes = video_file.read()
                    st.session_state.video_ready = True
                    status.update(label="Media unlocked successfully", state="complete")
                    st.toast("Ready to download.", icon="✅")
                else:
                    status.update(label="Could not process this media", state="error")
                    st.toast("Processing failed. Try another link.", icon="❌")
            except Exception:
                status.update(label="Unlock failed", state="error")
                st.toast("Fetch failed. Please try again.", icon="❌")

st.markdown(
    """
    <div class="how-to-card">
        <div class="how-to-title">How to use</div>
        <p class="how-to-item">🔗 Paste a media URL in the input field.</p>
        <p class="how-to-item">🟣 Tap <strong>Unlock Media</strong> to fetch the best version.</p>
        <p class="how-to-item">🌊 Tap <strong>Download MP4</strong> once it becomes active.</p>
    </div>
    """,
    unsafe_allow_html=True,
)