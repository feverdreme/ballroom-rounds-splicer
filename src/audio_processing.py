import subprocess
import os
from src.song import Song

def ffmpeg_trim(songs: list[Song | None]) -> None:
    for song in songs:
        if song is None:
            continue

        subprocess.run([
            "./ffmpeg",
            "-hide_banner", "-loglevel", "error",
            "-i", song.get_path(),
            "-ss", "00:00:00",
            "-t", "00:01:30",
            "-af", "afade=t=in:st=0:d=5,afade=out:st=85:d=5",
            "-y", # Overwrite
            song.get_trimmed_path()
        ])

def generate_silence(output_path: str, break_duration: str) -> None:
    subprocess.run([
        "./ffmpeg",
        "-hide_banner", "-loglevel", "error",
        "-f", "lavfi",
        "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-t", break_duration,
        "-acodec", "libmp3lame",
        "-y",
        output_path
    ], check=True)

def seconds_to_ffpmeg_time(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02}:{minutes:02}:{secs:02}"

def ffmpeg_concat(songs: list[Song | None], artifacts_path: str, output_path: str, break_duration: int = 10) -> None:
    """
    Concatenate MP3 files with breaks. None entries in songs list represent breaks.
    """
    silence_path = f"silence.mp3"
    concat_list_path = f"{artifacts_path}/concat_list.txt"
    
    break_duration_ffmpeg_time = seconds_to_ffpmeg_time(break_duration)
    generate_silence(f"{artifacts_path}/{silence_path}", break_duration_ffmpeg_time)
    
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
