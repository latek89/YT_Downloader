# playlist_downloader.py
from pytubefix import Playlist

def download_playlist(url):
    pl = Playlist(url)

    print(f"Playlist: {pl.title}")
    print(f"Liczba filmów: {len(pl.video_urls)}")

    for video in pl.videos:
        print(f"Pobieram: {video.title}")
        stream = video.streams.get_highest_resolution()
        stream.download()
        print("OK")
