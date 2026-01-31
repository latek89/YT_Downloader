# gui.py
import tkinter as tk
from tkinter import ttk, filedialog
import threading

from YT_Downloader import (
    list_video_qualities,
    list_audio_qualities,
    download_video,
    download_audio
)

selected_folder = ""
video_itags = {}
audio_itags = {}

def choose_folder():
    global selected_folder
    selected_folder = filedialog.askdirectory()
    if selected_folder:
        folder_label.config(text=f"Folder: {selected_folder}")
    else:
        folder_label.config(text="Folder: nie wybrano")

def load_qualities():
    link = entry.get().strip()
    mode = mode_var.get()

    quality_box.set("")
    quality_box['values'] = []
    status_label.config(text="")

    if not link:
        status_label.config(text="Wklej link!")
        return

    try:
        if mode == "video":
            qualities = list_video_qualities(link)
            global video_itags
            video_itags = {res: itag for res, itag in qualities}
            quality_box['values'] = list(video_itags.keys())

        elif mode == "audio":
            qualities = list_audio_qualities(link)
            global audio_itags
            audio_itags = {abr: itag for abr, itag in qualities}
            quality_box['values'] = list(audio_itags.keys())

        status_label.config(text="Jakości wczytane.")

    except Exception as e:
        status_label.config(text=f"Błąd: {e}")

def update_download_progress(percent):
    progress_bar_download['value'] = percent
    root.update_idletasks()

def update_merge_progress(percent):
    progress_bar_merge['value'] = percent
    root.update_idletasks()

def threaded_download():
    link = entry.get().strip()
    mode = mode_var.get()
    selected = quality_box.get()

    if not link:
        status_label.config(text="Wklej link!")
        return

    if not selected_folder:
        status_label.config(text="Wybierz folder zapisu!")
        return

    try:
        if mode == "video":
            if not selected:
                status_label.config(text="Wybierz jakość wideo!")
                return
            itag = video_itags[selected]
            download_video(
                link,
                itag,
                selected_folder,
                progress_callback=update_download_progress,
                merge_callback=update_merge_progress
            )

        elif mode == "audio":
            if not selected:
                status_label.config(text="Wybierz jakość audio!")
                return
            itag = audio_itags[selected]
            download_audio(link, itag, selected_folder, update_download_progress)

        status_label.config(text="Zakończono!")
        progress_bar_download['value'] = 100
        progress_bar_merge['value'] = 100

    except Exception as e:
        status_label.config(text=f"Błąd: {e}")

def start_download():
    progress_bar_download['value'] = 0
    progress_bar_merge['value'] = 0
    status_label.config(text="Pobieranie...")
    t = threading.Thread(target=threaded_download)
    t.daemon = True
    t.start()

root = tk.Tk()
root.title("YouTube Downloader")

tk.Label(root, text="Wklej link:").pack(pady=5)

entry = tk.Entry(root, width=60)
entry.pack()

mode_var = tk.StringVar(value="video")

mode_frame = tk.Frame(root)
mode_frame.pack(pady=5)

ttk.Radiobutton(mode_frame, text="Wideo", variable=mode_var, value="video").pack(side=tk.LEFT, padx=5)
ttk.Radiobutton(mode_frame, text="Audio (mp3)", variable=mode_var, value="audio").pack(side=tk.LEFT, padx=5)

tk.Button(root, text="Wczytaj dostępne jakości", command=load_qualities).pack(pady=5)

quality_box = ttk.Combobox(root, width=30, state="readonly")
quality_box.pack()

tk.Button(root, text="Wybierz folder zapisu", command=choose_folder).pack(pady=5)

folder_label = tk.Label(root, text="Folder: nie wybrano")
folder_label.pack()

tk.Label(root, text="Postęp pobierania:").pack()
progress_bar_download = ttk.Progressbar(root, length=350)
progress_bar_download.pack(pady=5)

tk.Label(root, text="Postęp łączenia audio + video:").pack()
progress_bar_merge = ttk.Progressbar(root, length=350)
progress_bar_merge.pack(pady=5)

tk.Button(root, text="Pobierz", command=start_download).pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack(pady=5)

root.mainloop()
