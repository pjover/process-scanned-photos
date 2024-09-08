import argparse
import os
from pathlib import Path

from directory_scanner import DirectoryScanner
from photo_processor import PhotoProcessor

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=
        "Script that processes scanned photos, so they can be easily imported to Lightroom."
        "See the README file at https://github.com/pjover/process-scanned-photos for more details."
    )
    parser.add_argument('dir', default=os.getcwd())
    parser.add_argument("-n", "--number", default=1, help="Initial photo number")
    parser.add_argument("-p", "--prefix", default="NEG", help="Prefix for the files")
    parser.add_argument("-d", "--dry_run", action="store_true", help="Dry run, do not process files")

    args = parser.parse_args()

    _target_dir = Path(args.dir)
    if not _target_dir.exists():
        print(f"❌ Directory does not exist")
        exit(1)

    _dry_run = args.dry_run
    if _dry_run:
        print("⚠️ Dry run, no files will be changed")

    photos = DirectoryScanner(_target_dir).process()
    PhotoProcessor(args.number, args.prefix, _dry_run).process(photos)
