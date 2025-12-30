import argparse
from src.roundlist import RoundList
from src.song import RoundBreak, Song
from src.audio_processing import ffmpeg_trim, ffmpeg_concat

from dataclasses import dataclass

@dataclass
class Arguments:
    sources: str
    output_path: str
    artifacts_dir: str
    download: bool
    multithreaded: bool
    ffmpeg_path: str

def parse_arguments() -> Arguments:
    parser = argparse.ArgumentParser(description="Process songs from a source file and optional download/processing options.")
    parser.add_argument('-s', '--sources', type=str, default='test/sources.txt',
                        help='The path to the sources file.')
    parser.add_argument('-o', '--output', type=str, default="rounds.mp3", help="Name of the output file (must be mp3).")
    parser.add_argument('-a', '--artifacts_dir', type=str, default='test/artifacts',
                        help='The path of artifacts and eventual output.')
    parser.add_argument('-d', '--download', action=argparse.BooleanOptionalAction,
                        help='Whether to download the songs from sources.',
                        default=True)
    parser.add_argument('-m', '--multithreaded', action=argparse.BooleanOptionalAction,
                        help='Whether to multithread downloading and processing audio.',
                        default=True)
    parser.add_argument("--ffmpeg-path", type=str, help="If manually specified, the local path of the ffmpeg binary.")

    args = parser.parse_args()

    return Arguments(
        sources=args.sources,
        output_path=args.output,
        artifacts_dir=args.artifacts_dir,
        download=args.download,
        multithreaded=args.multithreaded,
        ffmpeg_path=args.ffmpeg_path
    )

def main():
    cmd_args = parse_arguments()
    roundlist = RoundList(artifacts_dir=cmd_args.artifacts_dir, ffmpeg_path=cmd_args.ffmpeg_path)
    roundlist.parse_source_file(cmd_args.sources)
    roundlist.generate_artifacts(cmd_args.download, 10 if cmd_args.multithreaded else 1)

    for song in roundlist.get_songs():
        ffmpeg_trim(song.get_path(), song.get_trimmed_path(), cmd_args.ffmpeg_path)

    sourcelist: list[str] = []
    for rounditem in roundlist.get_order():
        if isinstance(rounditem, RoundBreak):
            sourcelist.append(f"break_{rounditem.duration}.mp3")
        elif isinstance(rounditem, Song):
            sourcelist.append(rounditem.get_trimmed_name())
        else:
            raise ValueError(f"Unknown round item type: {type(rounditem)}")

    ffmpeg_concat(sourcelist, cmd_args.artifacts_dir, cmd_args.output_path, cmd_args.ffmpeg_path)
    print("Success!")

if __name__ == "__main__":
    main()
