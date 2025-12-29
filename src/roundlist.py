import re

from src.song import RoundBreak, RoundItem, Song

class RoundList:
    def __init__(self, artifacts_dir: str = "test/artifacts", song_break: int = 10):
        self.items: list[RoundItem] = []
        self.artifacts_dir = artifacts_dir
        self.song_break = song_break
    
    def add_song(self, link: str):
        self.items.append(Song(link, len(self.items), self.artifacts_dir))
    
    def add_break(self, duration: int):
        self.items.append(RoundBreak(duration, len(self.items), self.artifacts_dir))
    
    def get_order(self) -> list[RoundItem]:
        # Need to include Song breaks
        result: list[RoundItem] = []
        for idx, item in enumerate(self.items):
            result.append(item)
            if not isinstance(item, Song):
                continue

            # Insert a break after each song unless it's the last item or next is already a break
            if idx + 1 < len(self.items):
                next_item = self.items[idx + 1]
                if not isinstance(next_item, RoundBreak):
                    result.append(RoundBreak(self.song_break, -1, self.artifacts_dir))
            else:
                # Last item; do not add trailing break
                pass

        return result
    
    def get_songs(self) -> list[Song]:
        return [item for item in self.get_order() if isinstance(item, Song)]
    
    @staticmethod
    def parse_source_file(source: str) -> RoundList:
        """
        Parse a source file and return a list of links.

        Example:
        ```
        # Waltz
        https://www.youtube.com/watch?v=dQw4w9WgXcQ
        # Tango
        https://www.youtube.com/watch?v=dQw4w9WgXcQ
        # Foxtrot
        https://www.youtube.com/watch?v=dQw4w9WgXcQ

        Break: 10

        # Cha Cha
        https://www.youtube.com/watch?v=dQw4w9WgXcQ
        # Jive
        https://www.youtube.com/watch?v=dQw4w9WgXcQ
        # Rumba
        https://www.youtube.com/watch?v=dQw4w9WgXcQ
        ```
        """
        roundlist = RoundList()

        spotify_youtube_regex = r'(?:https?:\/\/)?(?:www\.)?(?:(?:youtube\.com\/(?:watch\?v=|embed\/|shorts\/)|youtu\.be\/)[\w\-]+|(?:open\.)?spotify\.com\/(?:track|album|playlist|artist|episode|show)\/[\w]+|spotify\.link\/[\w]+|spoti\.fi\/[\w]+)'
        break_regex = r'Break:\s*(\d+)'
        
        with open(source, "r") as file:
            for line in file:
                line = line.strip()
                if re.match(spotify_youtube_regex, line):
                    roundlist.add_song(line)
                elif group := re.match(break_regex, line):
                    duration = int(group.group(1))
                    roundlist.add_break(duration)
                elif line.startswith("#") or len(line) == 0:
                    pass
                else:
                    print(f"Invalid link: {line}")
        
        return roundlist
