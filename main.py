import re
from typing import Generator, Iterable
import subprocess
import os

class Song:
    def __init__(self, link: str, index: int, artifacts_dir: str = "test/artifacts"):
        self.link = link
        self.index = index
        self.artifacts_dir = artifacts_dir
    
    def get_link(self) -> str:
        return self.link
    
    def get_artifact_path(self) -> str:
        return f"{self.artifacts_dir}/{self.index}.mp3"
    
    def get_trimmed_name(self) -> str:
        return f"{self.index}.trimmed.mp3"

    def get_trimmed_artifact_path(self) -> str:
        return f"{self.artifacts_dir}/{self.get_trimmed_name()}"
    

def parse_arguments() -> tuple[str, str]:
    # TODO: Use argparse to customize these
    input_path = "test/sources.txt"
    output_path = "test/artifacts"
    return input_path, output_path

def parse_source_file(source: str) -> Generator[Song | None, None, None]:
    """
    Parse a source file and return a list of links.

    A source file is a text file with one link per line.

    Example:
    ```
    https://www.youtube.com/watch?v=dQw4w9WgXcQ
    https://www.youtube.com/watch?v=dQw4w9WgXcQ
    ```

    Comments are allowed, and will be ignored. Only the links will be returned. Lines that are empty imply a break.

    Example:
    ```
    Waltz: https://www.youtube.com/watch?v=dQw4w9WgXcQ
    Tango: https://www.youtube.com/watch?v=dQw4w9WgXcQ
    Foxtrot: https://www.youtube.com/watch?v=dQw4w9WgXcQ
    Cha Cha: https://www.youtube.com/watch?v=dQw4w9WgXcQ

    Jive: https://www.youtube.com/watch?v=dQw4w9WgXcQ
    Rumba: https://www.youtube.com/watch?v=dQw4w9WgXcQ
    ```
    """
    spotify_youtube_regex = r'(?:https?:\/\/)?(?:www\.)?(?:(?:youtube\.com\/(?:watch\?v=|embed\/|shorts\/)|youtu\.be\/)[\w\-]+|(?:open\.)?spotify\.com\/(?:track|album|playlist|artist|episode|show)\/[\w]+|spotify\.link\/[\w]+|spoti\.fi\/[\w]+)'

    with open(source, "r") as file:
        for i, line in enumerate(file):
            line = line.strip()
            if line:
                matches = re.findall(spotify_youtube_regex, line)
                if len(matches) == 1:
                    yield Song(link=matches[0], index=i)
                elif len(matches) > 1:
                    print(f"Multiple links found in line: {line}")
                else:
                    print(f"Invalid link: {line}")
            else:
                yield None

def download_song(song: Song) -> None:
    subprocess.run(["spotdl", 
        "download", 
        song.get_link(),
        "--format",
        "mp3",
        "--output",
        song.get_artifact_path().replace("mp3", "{output-ext}")
    ])

def download_sequential_links(songs: Iterable[Song | None]):
    import threading

    threads: list[threading.Thread] = []
    for song in songs:
        if song is None:
            continue

        thread = threading.Thread(target=download_song, args=(song,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def ffmpeg_trim(songs: list[Song | None]) -> None:
    for song in songs:
        if song is None:
            continue

        subprocess.run([
            "./ffmpeg",
            "-hide_banner", "-loglevel", "error",
            "-i", song.get_artifact_path(),
            "-ss", "00:00:00",
            "-t", "00:01:30",
            "-af", "afade=t=in:st=0:d=5,afade=out:st=85:d=5",
            "-y", # Overwrite
            song.get_trimmed_artifact_path()
        ])

def ffmpeg_concat(songs: list[Song | None], output_path: str, break_duration: str = "00:00:05") -> None:
    """
    Concatenate MP3 files with breaks. None entries in songs list represent breaks.
    """
    artifacts_dir = os.path.dirname(output_path)
    silence_path = f"silence.mp3"
    concat_list_path = f"{artifacts_dir}/concat_list.txt"
    
    # Generate silence file
    subprocess.run([
        "./ffmpeg",
        "-hide_banner", "-loglevel", "error",
        "-f", "lavfi",
        "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-t", break_duration,
        "-acodec", "libmp3lame",
        "-y",
        f"{artifacts_dir}/{silence_path}"
    ], check=True)
    
    # Create concat file list
    with open(concat_list_path, "w+") as f:
        for song in songs:
            if song is None:
                # None represents a break
                f.write(f"file '{silence_path}'\n")
            else:
                f.write(f"file '{song.get_trimmed_name()}'\n")
    
    # Use concat demuxer
    subprocess.run([
        "./ffmpeg",
        "-hide_banner", "-loglevel", "error",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_path,
        "-c:a", "libmp3lame",  # Re-encode instead of copy
        "-b:a", "192k",  # Optional: set bitrate
        "-y",
        output_path
    ], check=True)

def clean_artifacts(audio_files: list[str]) -> None:
    for audio_file in audio_files:
        os.remove(audio_file)

def main():
    input_path, output_path = parse_arguments()
    songs = list(parse_source_file(input_path))

    # download_sequential_links(songs)

    ffmpeg_trim(songs)
    ffmpeg_concat(songs, "test/artifacts/concat.mp3")

if __name__ == "__main__":
    main()
