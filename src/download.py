import subprocess
from typing import Iterable
from src.song import Song

def download_song(song: Song):
    subprocess.run(["spotdl", 
        "download", 
        song.get_link(),
        "--format",
        "mp3",
        "--output",
        song.get_path().replace("mp3", "{output-ext}")
    ])

def download_sequential_links(songs: Iterable[Song]):
    import threading

    threads: list[threading.Thread] = []
    for song in songs:
        thread = threading.Thread(target=download_song, args=(song,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
