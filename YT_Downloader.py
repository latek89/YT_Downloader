from pytubefix import YouTube
from sys import argv

if len(argv) < 2:
    link = input("Podaj link do filmu: ")
else:
    link = argv[1]

yt = YouTube(link)

print("Title:", yt.title)
print("Views:", yt.views)


print("\nDostępne jakości wideo:")
streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()

for i, stream in enumerate(streams):
    print(f"{i+1}. {stream.resolution} - {stream.mime_type}")

choice = int(input("\nWybierz jakość (numer): "))
selected_stream = streams[choice - 1]

print("\nPobieranie wideo...")
selected_stream.download()
print("Zakończono!")

# Pobieranie audio
audio_choice = input("\nCzy chcesz pobrać audio (mp3)? (t/n): ")

if audio_choice.lower() == "t":
    audio = yt.streams.filter(only_audio=True).first()
    print("Pobieranie audio...")
    audio.download(filename=f"{yt.title}.mp3")
    print("Audio pobrane!")


# Obsługa Biblioteki

from pytubefix import Playlist

url = input("Podaj link do playlisty: ")
pl = Playlist(url)

print(f"\nPlaylist: {pl.title}")
print(f"Liczba filmów: {len(pl.video_urls)}")

for video in pl.videos:
    print(f"Pobieram: {video.title}")
    video.streams.get_highest_resolution().download()


#GUI thinker dla YT downloadera


import tkinter as tk
from pytubefix import YouTube

def download_video():
    link = entry.get()
    yt = YouTube(link)
    stream = yt.streams.get_highest_resolution()
    stream.download()
    label_status.config(text="Pobrano!")

root = tk.Tk()
root.title("YouTube Downloader")

label = tk.Label(root, text="Wklej link:")
label.pack()

entry = tk.Entry(root, width=50)
entry.pack()

button = tk.Button(root, text="Pobierz wideo", command=download_video)
button.pack()

label_status = tk.Label(root, text="")
label_status.pack()

root.mainloop()
