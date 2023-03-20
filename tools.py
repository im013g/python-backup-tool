#!/usr/bin/env python3

import os
import time
import json
import stat

def get_nested_files(directory: str) -> list:
    result = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            result.append(os.path.join(root, file))
    return result

def import_json(json_filepath: str):
    result = None
    with open(json_filepath, "r") as infile:
        result = json.load(infile)
    return result

def export_json(json_filepath: str, body, indent: int = 2):
    json_object = None
    json_object = json.dumps(body, indent=indent)
    with open(json_filepath, "w") as outfile:
        outfile.write(json_object)

def generate_file_metadata(filepath: str) -> dict:
    result = {}

    # print()
    # print(filepath)

    # Get the file inode
    inode_num = os.lstat(filepath)[stat.ST_INO]
    # print(f'File inode number: {inode_num}')

    # Get the file creation time
    ctime_unix = os.path.getctime(filepath)
    ctime_human = time.ctime(ctime_unix)
    # print(f'File creation UNIX time: {ctime_unix}')
    # print(f'File creation human time: {ctime_human}')

    # Get the file modification time
    mtime_unix = os.path.getmtime(filepath)
    mtime_human = time.ctime(mtime_unix)
    # print(f'File modification UNIX time: {mtime_unix}')
    # print(f'File modification human time: {mtime_human}')

    result = {
        'filepath': filepath,
        'inode_num': inode_num,
        'ctime_unix': ctime_unix,
        'mtime_unix': mtime_unix,
        'ctime_human': ctime_human,
        'mtime_human': mtime_human
    }
    return result


def main():
    print()
    source_dir_location = "test_dir"
    file_list = []
    source_dir_metadata = []

    file_list = get_nested_files(directory = source_dir_location)

    for path in file_list:
        source_dir_metadata.append(generate_file_metadata(filepath = path))

    # print(source_dir_metadata)
    export_json(json_filepath='source_dir_metadata.json', body=source_dir_metadata)


if __name__ == '__main__':
    main()