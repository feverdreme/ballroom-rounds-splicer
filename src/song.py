from typing import Optional


class Song:
    def __init__(self, link: str, index: int, artifacts_dir: str = "test/artifacts"):
        self.link = link
        self.index = index
        self.artifacts_dir = artifacts_dir
    
    def get_link(self) -> str:
        return self.link
    
    def get_path(self) -> str:
        return f"{self.artifacts_dir}/{self.index}.mp3"
    
    def get_trimmed_name(self) -> str:
        return f"{self.index}.trimmed.mp3"

    def get_trimmed_path(self) -> str:
        return f"{self.artifacts_dir}/{self.get_trimmed_name()}"