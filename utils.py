#!/usr/bin/env python3

import os
import time
import json
import stat
import shutil
import pwd
import grp


# def get_nested_files(directory: str) -> list:
#     result = []
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             result.append(os.path.join(root, file))
#     return result


def get_filesystem_nested_items(directory: str, 
                                return_files: bool = True, 
                                return_dirs: bool = True, 
                                return_absolute_paths: bool = False) -> list:
    pre_result = []
    result = []
    for root, dirs, files in os.walk(directory):
        if return_files:
            for file in files:
                pre_result.append(os.path.join(root, file))
        if return_dirs:
            for dir in dirs:
                pre_result.append(os.path.join(root, dir))
    if not return_absolute_paths:
        if return_files or return_dirs:
            for path in pre_result:
                result.append(os.path.relpath(path, directory))
    else:
        result = pre_result
    return result


def get_nested_files(directory: str) -> list:
    result = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            result.append(os.path.join(root, file))
    return result


def check_file_exists(file_path: str) -> bool:
    result = bool
    result = os.path.isfile(file_path)
    return result


def import_json(json_file_path: str):
    result = None
    with open(json_file_path, "r") as infile:
        result = json.load(infile)
    return result


def export_json(json_file_path: str, body, indent: int = 2):
    json_object = None
    json_object = json.dumps(body, indent=indent)
    with open(json_file_path, "w") as outfile:
        outfile.write(json_object)


def generate_file_metadata(root_path: str, file_path: str, return_absolute_paths: bool = False) -> dict:
    # print(file_path)
    result = {}
    result_file_path = ""
    item_type = ""
    absolute_file_path = f'{root_path}/{file_path}'
    inode_num = os.lstat(absolute_file_path)[stat.ST_INO]
    ctime_unix = os.path.getctime(absolute_file_path)
    ctime_human = time.ctime(ctime_unix)
    mtime_unix = os.path.getmtime(absolute_file_path)
    mtime_human = time.ctime(mtime_unix)
    uid = os.stat(absolute_file_path).st_uid
    gid = os.stat(absolute_file_path).st_gid
    owner = pwd.getpwuid(uid).pw_name
    group = grp.getgrgid(gid).gr_name
    if return_absolute_paths:
        result_file_path = absolute_file_path
    else:
        result_file_path = file_path
    if os.path.isfile(absolute_file_path):
        item_type = 'file'
    elif os.path.isdir(absolute_file_path):
        item_type = 'directory'
    else:
        item_type = 'unknown'
    result = {
        'file_path': result_file_path,
        'type': item_type,
        'inode_num': inode_num,
        'ctime_unix': ctime_unix,
        'mtime_unix': mtime_unix,
        'ctime_human': ctime_human,
        'mtime_human': mtime_human,
        'uid': uid,
        'gid': gid,
        'owner': owner,
        'group': group 
    }
    return result


def generate_dir_metadata(dir_path: str, return_absolute_paths: bool = False) -> list:
    item_paths = []
    result = []
    # item_paths = get_nested_files(directory = dir_path)
    item_paths = get_filesystem_nested_items(directory=dir_path)
    for path in item_paths:
        result.append(generate_file_metadata(root_path = dir_path, file_path = path))
    return result


def get_file_metadata_from_state(state: list, file_path: str):
    result = {}
    for entry in state:
        if file_path == entry['file_path']:
            result = entry
            break
    return result


def copy_files(source_dir_metadata: list, source_path: str, target_path: str, preserve_ownership: bool):
    for entry in source_dir_metadata:
        # print(entry['file_path'])
        # shutil.copy(entry['file_path'], target_path)
        # target_result_path = os.path.join(target_path, os.path.relpath(entry['file_path'], source_path))
        os.makedirs(os.path.dirname(f'''{target_path}/{entry['file_path']}'''), exist_ok=True)
        shutil.copy(f'''{source_path}/{entry['file_path']}''', f'''{target_path}/{entry['file_path']}''')
        if preserve_ownership:
            os.chown(target_result_path, entry['uid'], entry['gid'])


def copy_file(source_path: str, source_metadata: dict, target_path: str, preserve_ownership: bool):
    # target_result_path = os.path.join(target_path, os.path.relpath(entry['file_path'], source_path))

    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    shutil.copy(source_path, target_path)
    if preserve_ownership:
        os.chown(target_path, source_metadata['uid'], source_metadata['gid'])

        # print(target_result_path)
        # print(f'''{entry['file_path']} --> {target_result_path}''')


