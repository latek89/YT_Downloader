# YT_Downloader.py
import os
import subprocess
from pytubefix import YouTube

# >>> 1. FUNKCJA CZYSZCZĄCA NAZWĘ PLIKU <<<
def safe_filename(name):
    forbidden = r'\/:*?"<>|'
    for char in forbidden:
        name = name.replace(char, "_")
    return name

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FFMPEG_PATH = os.path.join(BASE_DIR, "ffmpeg", "bin", "ffmpeg.exe")

def on_progress(stream, chunk, bytes_remaining, progress_callback=None):
    if progress_callback:
        total = stream.filesize
        percent = int((total - bytes_remaining) * 100 / total)
        progress_callback(percent)

def list_video_qualities(link):
    yt = YouTube(link)
    streams = yt.streams.filter(type="video", file_extension='mp4').order_by('resolution').desc()
    unique = {}
    for s in streams:
        unique[s.resolution] = s.itag
    return list(unique.items())

def list_audio_qualities(link):
    yt = YouTube(link)
    streams = yt.streams.filter(only_audio=True).order_by('abr').desc()
    unique = {}
    for s in streams:
        unique[s.abr] = s.itag
    return list(unique.items())

def merge_audio_video(video_path, audio_path, output_path, merge_callback=None):
    command = [
        FFMPEG_PATH,
        "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        output_path
    ]

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        encoding="utf-8",
        errors="ignore"
    )

    for line in process.stdout:
        if "time=" in line and merge_callback:
            merge_callback(50)

    process.wait()

    if merge_callback:
        merge_callback(100)

def download_video(link, itag, folder, progress_callback=None, merge_callback=None):
    yt = YouTube(link, on_progress_callback=lambda s, c, r: on_progress(s, c, r, progress_callback))

    video_stream = yt.streams.get_by_itag(itag)
    audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

    video_path = os.path.join(folder, "temp_video.mp4")
    audio_path = os.path.join(folder, "temp_audio.mp3")

    # >>> 2. TU UŻYWAMY safe_filename DLA WIDEO <<<
    output_path = os.path.join(folder, f"{safe_filename(yt.title)}.mp4")

    video_stream.download(output_path=folder, filename="temp_video.mp4")
    audio_stream.download(output_path=folder, filename="temp_audio.mp3")

    merge_audio_video(video_path, audio_path, output_path, merge_callback)

    os.remove(video_path)
    os.remove(audio_path)

def download_audio(link, itag, folder, progress_callback=None):
    yt = YouTube(link, on_progress_callback=lambda s, c, r: on_progress(s, c, r, progress_callback))
    stream = yt.streams.get_by_itag(itag)

    # >>> 3. TU UŻYWAMY safe_filename DLA AUDIO <<<
    stream.download(output_path=folder, filename=f"{safe_filename(yt.title)}.mp3")
