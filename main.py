import re
import os
import argparse
from typing import Generator
from src.download import download_sequential_links
from src.song import Song
from src.audio_processing import ffmpeg_trim, ffmpeg_concat

from dataclasses import dataclass

@dataclass
class Arguments:
    sources: str
    output_path: str
    artifacts_dir: str
    download: bool
    multithreaded: bool

def parse_arguments() -> Arguments:
    """
    Must handle the following usage:
    -s, --sources The path to the sources file. Default is "test/sources.txt".
    -a, --artifacts_dir The path of artifacts and eventual output. Default is "test/artifacts".
    -d, --download A boolean variable whether to download the songs from sources.
    -m, --multithreaded A boolean variable whether to multithread downloading and processing audio.
    """
    parser = argparse.ArgumentParser(description="Process songs from a source file and optional download/processing options.")
    parser.add_argument('-s', '--sources', type=str, default='test/sources.txt',
                        help='The path to the sources file.')
    parser.add_argument('-a', '--artifacts_dir', type=str, default='test/artifacts',
                        help='The path of artifacts and eventual output.')
    parser.add_argument('-d', '--download', action=argparse.BooleanOptionalAction,
                        help='Whether to download the songs from sources.',
                        default=False)
    parser.add_argument('-m', '--multithreaded', action=argparse.BooleanOptionalAction,
                        help='Whether to multithread downloading and processing audio.',
                        default=False)

    args = parser.parse_args()

    # Determine output file path based on artifacts_dir
    output_path = os.path.join(args.artifacts_dir, "output.mp3")

    return Arguments(
        sources=args.sources,
        output_path=output_path,
        artifacts_dir=args.artifacts_dir,
        download=args.download,
        multithreaded=args.multithreaded
    )

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

def main():
    cmd_args = parse_arguments()
    songs = list(parse_source_file(cmd_args.sources))

    if cmd_args.download:
        download_sequential_links(songs)

    ffmpeg_trim(songs)
    ffmpeg_concat(songs, f"{cmd_args.artifacts_dir}/concat.mp3")

if __name__ == "__main__":
    main()
