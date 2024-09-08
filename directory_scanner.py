import os
import re
from datetime import datetime
from os import listdir
from os.path import isfile, join
from pathlib import Path

from Photo import Photo


class DirectoryScanner:
    folder_regex = r"([0-9]{2})-([0-9]{2}).*"
    photo_regex = r".*-([0-9]{1,2}).ti[f]{1,2}"

    def __init__(self, target_dir: Path):
        self._target_dir = target_dir

    def process(self) -> list[Photo]:
        photos = []
        errors = []
        for year in self._read_years():
            _photos, _errors = self._process_year(year)
            photos.extend(_photos)
            errors.extend(_errors)

        if errors:
            print("Errors:")
            for error in errors:
                print(error)
            return []

        return photos

    def _read_years(self, ) -> list[int]:
        years = [
            int(f) for f in listdir(self._target_dir) if
            not f.startswith(".")
            and os.path.isdir(os.path.join(self._target_dir, f))
            and f.isnumeric()
        ]
        return sorted(years)

    def _process_year(self, year: int) -> tuple[list[Photo], list[str]]:
        photos = []
        errors = []
        for folder in self._read_folders(year):
            _photos, _errors = self._read_folder(year, folder)
            photos.extend(_photos)
            errors.extend(_errors)
        return photos, errors

    def _read_folders(self, year: int):
        year_folder_path = os.path.join(self._target_dir, str(year))
        folders = [
            f for f in listdir(year_folder_path) if
            not f.startswith(".")
            and os.path.isdir(os.path.join(year_folder_path, f))
        ]
        return sorted(folders)

    def _read_folder(self, year: int, folder_name: str) -> tuple[list[Photo], list[str]]:
        folder: Path = Path(os.path.join(os.path.join(self._target_dir, str(year)), folder_name))
        month, day = re.findall(self.folder_regex, folder_name)[0]
        date_time = datetime(year, int(month), int(day), 0, 0)
        return self._read_photos(date_time, folder)

    def _read_photos(self, date_time: datetime, folder: Path) -> tuple[list[Photo], list[str]]:
        errors: list[str] = []
        files = [
            f for f in listdir(folder) if
            not f.startswith(".")
            and isfile(join(folder, f))
            and f.__contains__(".tif")
        ]
        if not files:
            print(f"⚠️ No photos found in {folder}")
            return [], []

        photos = []
        for filename in files:
            photo, err = self._get_photo(date_time, folder, filename)
            if err:
                errors.append(err)
            if photo:
                photos.append(photo)
        return sorted(photos, key=lambda x: x.index), errors

    def _get_photo(self, date_time: datetime, folder: Path, filename: str) -> tuple[Photo or None, str or None]:
        try:
            index = int(re.findall(self.photo_regex, filename)[0])
        except IndexError:
            return None, f"🔴 Invalid file name {filename} at {folder}"
        return Photo(index, folder, filename, date_time), None
