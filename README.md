# python-backup-tool

## Plan

1. Gather metadata from source and target folders. +

2. The target directory structure will be created +

3. Check if previous state for source exists == True

3.1 Compare current with prevoius.
3.2 If metadata !=, file changed, copy file with creating dir structure.
3.3 If metadata ==, check the metadata of the same file on target. Copy file if metadata !=, or file is absent on target.
3.4 If no metadata in prevoius, copy file to target.
3.5 Compare previous with current.
3.6 If no file in current. The file was deleted from the source, it will be moved to the _BIN_ directory with today's date.

4. Check if previous state for source exists == False

4.1 Compare current with target.
4.2 If metadata !=, file changed, copy file.
4.3 If no target file, copy file.