import yt_dlp
import os
import traceback
import re
import tempfile
from pathlib import Path

def sanitize_filename(title):
    """Clean the title to make it filesystem-friendly"""
    # Remove invalid characters and trim spaces
    clean_title = re.sub(r'[<>:"/\\|?*]', '', title)
    clean_title = clean_title.strip()
    # Limit length to avoid too long filenames
    return clean_title[:100]

def download_audio(video_url, default_title="video"):
    """
    Download audio from a YouTube video.
    
    :param video_url: URL of the YouTube video
    :param default_title: Default title if none is found
    :return: Tuple of (file_path, video_title) or (None, None) if download fails
    """
    # Create temp directory if it doesn't exist
    temp_dir = tempfile.gettempdir()
    download_dir = Path(temp_dir) / "youtube_audio_downloads"
    download_dir.mkdir(exist_ok=True)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'outtmpl': str(download_dir / '%(title)s.%(ext)s'),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            video_title = info.get('title', default_title)
            base, _ = os.path.splitext(filename)
            wav_path = f"{base}.wav"
            return wav_path, sanitize_filename(video_title)
    except Exception as e:
        print(f"Error downloading audio: {str(e)}")
        print(traceback.format_exc())
        return None, None