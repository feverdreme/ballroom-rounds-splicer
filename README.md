# README.md

## Installation

To set up this project, follow these steps:

**Install dependencies using [uv](https://github.com/astral-sh/uv) (recommended):**

```bash
uv sync
```

**Download `ffmpeg` to the main directory:**

**On Linux/macOS:**

```bash
wget -O ffmpeg https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
tar -xf ffmpeg-release-amd64-static.tar.xz
cp ffmpeg-*-amd64-static/ffmpeg .
chmod +x ffmpeg
# Optionally clean up
rm -rf ffmpeg-*-amd64-static ffmpeg-release-amd64-static.tar.xz
```

**On Windows:**

1. Download the static build from https://www.gyan.dev/ffmpeg/builds/
2. Extract `ffmpeg.exe` and place it in the main directory of this project.
3. You may also rename it to `ffmpeg.exe` if needed.

**Note:** The code expects an `ffmpeg` (Linux/macOS) or `ffmpeg.exe` (Windows) binary in the project root directory.

## Usage

```bash
$ python3 main.py -h
usage: main.py [-h] [-s SOURCES] [-o OUTPUT] [-a ARTIFACTS_DIR] [-d | --download | --no-download]
               [-m | --multithreaded | --no-multithreaded]

Process songs from a source file and optional download/processing options.

options:
  -h, --help            show this help message and exit
  -s, --sources SOURCES
                        The path to the sources file.
  -o, --output OUTPUT   Name of the output file (must be mp3).
  -a, --artifacts_dir ARTIFACTS_DIR
                        The path of artifacts and eventual output.
  -d, --download, --no-download
                        Whether to download the songs from sources.
  -m, --multithreaded, --no-multithreaded
                        Whether to multithread downloading and processing audio.
```

## Example

You can run the following command to create the round defined by [test/sources2.txt](test/sources2.txt).

```bash
python3 main.py --sources test/sources2.txt --output rounds.mp3
```

which will create a `rounds.mp3` file in the main directory.

## Future Improvements

- [ ] Allow specifying an ffmpeg path and making the default behavior to call `ffmpeg`, not `./ffmpeg` as a subprocess.
- [ ] Allow downloading playlists and packaging them as rounds automatically.
- [ ] Allow putting playlists in a sources.txt.
- [ ] Create a system where a song library is maintained so the tool can look up a cache of songs to refernence in sources.txt.
- [ ] Test the tool for YouTube music.
- [ ] Allow the user to turn off multithreading.
- [ ] Prevent race condition of generating multiple breaks of the same duration.
- [ ] Make trimming concurrent.
- [ ] Perhaps rewrite the entire code base in OCaml because `|>` is cool. 🐫
- [ ] Add arguments for setting default song durations.
- [ ] Add ability to specify custom song durations and starts in sources.txt
- [ ] Add arguments for setting default song break durations.
