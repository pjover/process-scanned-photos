import os
from datetime import timedelta

from Photo import Photo


class PhotoProcessor:
    NUMBER_OF_DIGITS = 4

    def __init__(self, number: int, prefix: str, dry_run: bool):
        self._number = number
        self._prefix = prefix
        self._dry_run = dry_run
        self._counter = number

    def process(self, photos: list[Photo]):
        for photo in photos:
            self._process(photo)

    def _process(self, photo: Photo):
        old_name = photo.filename
        photo = self._rename(photo)
        photo = self._set_date_time(photo)
        msg = f"Processed {old_name} to {photo.filename} at {photo.date_time}"
        if self._dry_run:
            print("🟡 " + msg)
        else:
            print("🟢 " + msg)
        self._counter += 1

    def _rename(self, photo: Photo) -> Photo:
        new_name = f"{self._prefix}{self._counter:04d}.tiff"
        if not self._dry_run:
            os.rename(
                os.path.join(photo.folder, photo.filename),
                os.path.join(photo.folder, new_name)
            )
        photo.filename = new_name
        return photo

    def _set_date_time(self, photo: Photo) -> Photo:
        new_time = photo.date_time + timedelta(0, photo.index * 60)
        if not self._dry_run:
            os.utime(
                os.path.join(photo.folder, photo.filename),
                (new_time.timestamp(), new_time.timestamp())
            )
        photo.date_time = new_time
        return photo
