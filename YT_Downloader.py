# YT_Downloader.py
from pytubefix import YouTube

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

def download_video(link, itag, folder, progress_callback=None):
    yt = YouTube(link, on_progress_callback=lambda s, c, r: on_progress(s, c, r, progress_callback))
    stream = yt.streams.get_by_itag(itag)
    stream.download(output_path=folder)

def download_audio(link, itag, folder, progress_callback=None):
    yt = YouTube(link, on_progress_callback=lambda s, c, r: on_progress(s, c, r, progress_callback))
    stream = yt.streams.get_by_itag(itag)
    stream.download(output_path=folder, filename=f"{yt.title}.mp3")
