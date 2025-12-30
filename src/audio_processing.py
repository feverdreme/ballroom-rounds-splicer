import os
import subprocess

def ffmpeg_trim(source: str, dest: str) -> None:
    subprocess.run([
        "./ffmpeg",
        "-hide_banner", "-loglevel", "error",
        "-i", source,
        "-ss", "00:00:00",
        "-t", "00:01:30",
        "-af", "afade=t=in:st=0:d=5,afade=out:st=85:d=5",
        "-y", # Overwrite
        dest
    ])

def generate_silence(output_path: str, break_duration: str) -> None:
    if os.path.exists(output_path):
        print(f"{output_path} already exists. Skipping...")
        return

    args = [
        "./ffmpeg",
        "-hide_banner", "-loglevel", "error",
        "-f", "lavfi",
        "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-t", break_duration,
        "-acodec", "libmp3lame",
        output_path
    ]
    
    subprocess.run(args, check=True)

def seconds_to_ffpmeg_time(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02}:{minutes:02}:{secs:02}"

def ffmpeg_concat(sourcelist: list[str], artifacts_path: str, output_path: str) -> None:
    """
    Concatenate MP3 files with breaks. None entries in songs list represent breaks.
    """

    concat_list_path = f"{artifacts_path}/concat_list.txt"
    
    # Create concat file list
    with open(concat_list_path, "w+") as f:
        for source in sourcelist:
            f.write(f'file {source}\n')
    
    
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
