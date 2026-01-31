# YT_Downloader.py
from pytubefix import YouTube

def list_video_qualities(link):
    yt = YouTube(link)
    streams = yt.streams.filter(type="video", file_extension='mp4').order_by('resolution').desc()
    return [(s.resolution, s.itag) for s in streams]

def list_audio_qualities(link):
    yt = YouTube(link)
    streams = yt.streams.filter(only_audio=True).order_by('abr').desc()
    return [(s.abr, s.itag) for s in streams]

def download_video(link, itag):
    yt = YouTube(link)
    stream = yt.streams.get_by_itag(itag)
    print(f"Pobieranie wideo: {stream.resolution}")
    stream.download()
    print("Pobrano wideo!")

def download_audio(link, itag):
    yt = YouTube(link)
    stream = yt.streams.get_by_itag(itag)
    print(f"Pobieranie audio: {stream.abr}")
    stream.download(filename=f"{yt.title}.mp3")
    print("Audio pobrane!")
