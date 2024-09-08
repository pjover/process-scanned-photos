from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class Photo:
    index: int
    folder: Path
    filename: str
    date_time: datetime
