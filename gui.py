# gui.py
import tkinter as tk
from tkinter import ttk
from YT_Downloader import (
    list_video_qualities,
    list_audio_qualities,
    download_video,
    download_audio
)
from playlist_downloader import download_playlist

def load_qualities():
    link = entry.get()
    mode = mode_var.get()

    quality_box['values'] = []

    if mode == "video":
        qualities = list_video_qualities(link)
        quality_box['values'] = [q[0] for q in qualities]
        global video_itags
        video_itags = {q[0]: q[1] for q in qualities}

    elif mode == "audio":
        qualities = list_audio_qualities(link)
        quality_box['values'] = [q[0] for q in qualities]
        global audio_itags
        audio_itags = {q[0]: q[1] for q in qualities}

def start_download():
    link = entry.get()
    mode = mode_var.get()
    selected = quality_box.get()

    if mode == "video":
        itag = video_itags[selected]
        download_video(link, itag)

    elif mode == "audio":
        itag = audio_itags[selected]
        download_audio(link, itag)

    elif mode == "playlist":
        download_playlist(link)

    status_label.config(text="Zakończono!")

root = tk.Tk()
root.title("YouTube Downloader")

tk.Label(root, text="Wklej link:").pack()

entry = tk.Entry(root, width=50)
entry.pack()

mode_var = tk.StringVar(value="video")

ttk.Radiobutton(root, text="Wideo", variable=mode_var, value="video").pack()
ttk.Radiobutton(root, text="Audio (mp3)", variable=mode_var, value="audio").pack()
ttk.Radiobutton(root, text="Playlista", variable=mode_var, value="playlist").pack()

tk.Button(root, text="Wczytaj dostępne jakości", command=load_qualities).pack(pady=5)

quality_box = ttk.Combobox(root, width=30)
quality_box.pack()

tk.Button(root, text="Pobierz", command=start_download).pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
