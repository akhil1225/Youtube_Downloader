import streamlit as st
import yt_dlp
import os
import traceback


st.set_page_config(page_title="YouTube Downloader", layout="centered")


st.title("🎬 YouTube Audio/Video Downloader")
st.write(
    "Download YouTube videos as **MP3 (Audio)** or **MP4 (Video)** directly from your browser."
)

st.subheader("🔗 Enter YouTube Link")
url = st.text_input("Paste your YouTube URL below:")

st.subheader("🎚️ Choose Mode")
mode = st.radio("Select output type:", ("Audio (MP3)", "Video (MP4)"))

output_path = "downloads"
os.makedirs(output_path, exist_ok=True)


# download fn
def download_video(url, output_path, mode):
    try:
        if mode == "Audio (MP3)":
            ydl_opts = {
                "outtmpl": f"{output_path}/%(title)s.%(ext)s",
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
                "quiet": True,
                "ignoreerrors": False,
            }
        else:
            ydl_opts = {
    "outtmpl": f"{output_path}/%(title)s.%(ext)s",
    "format": "bestaudio/best",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
    "quiet": True,
    "ignoreerrors": False,
    "nocheckcertificate": True,
    "geo_bypass": True,
    "http_headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/116.0.0.0 Safari/537.36"
    },
}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            actual_file = ydl.prepare_filename(info)

            
            if mode == "Audio (MP3)":
                base, _ = os.path.splitext(actual_file)
                actual_file = base + ".mp3"
            else:
                base, _ = os.path.splitext(actual_file)
                actual_file = base + ".mp4"

            if not os.path.exists(actual_file):
                raise FileNotFoundError(f"yt_dlp reported file missing: {actual_file}")

            return actual_file

    except Exception as e:
        tb = traceback.format_exc()
        st.error(f"❌ **An error occurred during download.**\n\n**Error:** {str(e)}")
        with st.expander("Show technical details"):
            st.code(tb, language="python")
        return None


# download btn
if st.button("Start Download"):
    if not url.strip():
        st.warning("⚠️ Please enter a valid YouTube URL before downloading.")
    else:
        st.info("⏳ Downloading... Please wait while we process your request.")
        file_path = download_video(url, output_path, mode)

        if file_path and os.path.exists(file_path):
            st.success("✅ Download completed successfully!")
            with open(file_path, "rb") as f:
                if mode == "Audio (MP3)":
                    st.download_button(
                        label="⬇️ Download MP3 File",
                        data=f,
                        file_name=os.path.basename(file_path),
                        mime="audio/mpeg",
                    )
                else:
                    st.download_button(
                        label="⬇️ Download MP4 File",
                        data=f,
                        file_name=os.path.basename(file_path),
                        mime="video/mp4",
                    )
        else:
            st.error("❌ Something went wrong. Please check the error details above.")
