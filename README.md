# Process scanned photos

Script that processes scanned photos, so they can be easily imported to Lightroom:

1. Renames scanned photos in a directory and sub directories recursively

- The script will rename all files to 'NEG0001.tiff' like filenames.
- NEG is the prefix, 0001 is the photo number, that is correlative.
- Usual prefixes are NEG (negative) and DIA (diapositive).
- NEG is the default prefix.

2. Sets the creation and modification date

- The script will set the date and time for all photos, based on the parents folder structure.
- The parents folder structure must be named in the format `YYYY/MM-DD-Optional title/`.
- For every folder, the first folder photo is set at 00:01, following photos will be increased by one minute.
