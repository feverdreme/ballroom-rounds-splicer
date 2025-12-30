import subprocess
from src.audio_processing import generate_silence, seconds_to_ffpmeg_time
from src.rounditem import RoundItem

class Song(RoundItem):
    def __init__(self, link: str, index: int, artifacts_dir: str):
        super().__init__(index=index, artifacts_dir=artifacts_dir)

        self.link = link
    
    def get_link(self) -> str:
        return self.link
    
    def get_path(self) -> str:
        return f"{self.artifacts_dir}/{self.index}.mp3"
    
    def get_trimmed_name(self) -> str:
        return f"{self.index}.trimmed.mp3"

    def get_trimmed_path(self) -> str:
        return f"{self.artifacts_dir}/{self.get_trimmed_name()}"
    
    def generate_artifact(self):
        subprocess.run(["spotdl", 
            "download", 
            self.get_link(),
            "--format",
            "mp3",
            "--output",
            self.get_path().replace("mp3", "{output-ext}")
        ])

class RoundBreak(RoundItem):
    def __init__(self, duration: int, index: int, artifacts_dir):
        super().__init__(index=index, artifacts_dir=artifacts_dir)
        self.duration = duration

    def get_duration(self):
        return self.duration
    
    def get_path(self):
        return f"{self.artifacts_dir}/break_{self.duration}.mp3"
    
    def generate_artifact(self) -> None:
        break_duration_ffmpeg_time = seconds_to_ffpmeg_time(self.duration)
        generate_silence(self.get_path(), break_duration_ffmpeg_time)
