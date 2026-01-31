# playlist_downloader.py
from pytubefix import Playlist

def download_playlist(url, folder, progress_callback=None):
    pl = Playlist(url)

    for video in pl.videos:
        stream = video.streams.get_highest_resolution()
        stream.download(output_path=folder)
        if progress_callback:
            progress_callback(100)
