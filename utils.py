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

def check_file_exists(item_path: str) -> bool:
    result = bool
    result = os.path.isfile(item_path)
    return result

def check_dir_exists(item_path: str) -> bool:
    result = bool
    result = os.path.isdir(item_path)
    return result

def import_json(json_item_path: str):
    result = None
    with open(json_item_path, "r") as infile:
        result = json.load(infile)
    return result


def export_json(json_item_path: str, body, indent: int = 2):
    json_object = None
    json_object = json.dumps(body, indent=indent)
    with open(json_item_path, "w") as outfile:
        outfile.write(json_object)


def generate_file_metadata(root_path: str, item_path: str, return_absolute_paths: bool = False) -> dict:
    # print(item_path)
    result = {}
    result_item_path = ""
    item_type = ""
    absolute_item_path = f'{root_path}/{item_path}'
    inode_num = os.lstat(absolute_item_path)[stat.ST_INO]
    ctime_unix = os.path.getctime(absolute_item_path)
    ctime_human = time.ctime(ctime_unix)
    mtime_unix = os.path.getmtime(absolute_item_path)
    mtime_human = time.ctime(mtime_unix)
    uid = os.stat(absolute_item_path).st_uid
    gid = os.stat(absolute_item_path).st_gid
    owner = pwd.getpwuid(uid).pw_name
    group = grp.getgrgid(gid).gr_name
    if return_absolute_paths:
        result_item_path = absolute_item_path
    else:
        result_item_path = item_path
    if os.path.isfile(absolute_item_path):
        item_type = 'file'
    elif os.path.isdir(absolute_item_path):
        item_type = 'directory'
    else:
        item_type = 'unknown'
    result = {
        'item_path': result_item_path,
        'type': item_type,
        'mtime_unix': mtime_unix,
        'mtime_human': mtime_human,
        'uid': uid,
        'gid': gid,
        'owner': owner,
        'group': group 
    }
    return result

def generate_dir_metadata(dir_path: str, ignore_names: list):
    item_paths = []
    result = {
        'files': {},
        'directories': {}
    }
    item_paths = get_filesystem_nested_items(directory=dir_path)
    for path in item_paths:
        if path not in ignore_names:
            path_metadata = generate_file_metadata(root_path = dir_path, item_path = path)
            if path_metadata['type'] == 'file':
                result['files'][path] = path_metadata
            elif path_metadata['type'] == 'directory':
                result['directories'][path] = path_metadata
    return result


def get_file_metadata_from_state(file_metadata: dict, state_body: str):
    """
    Search file metadata in state. Accepts metadata as searcg criteria.
    Returns found file metadata dict.
    """
    result = {}
    item_path = ""
    item_path = file_metadata['item_path']
    for entry in state_body:
        if item_path == entry['item_path']:
            result = entry
            break
    return result


def copy_directory(source_item_metadata: dict, target_path: str, preserve_metadata: bool = False):
    item_path = source_item_metadata['item_path']
    item_uid = source_item_metadata['uid']
    item_gid = source_item_metadata['gid']
    item_mtime = source_item_metadata['mtime_unix']
    if source_item_metadata['type'] == 'directory':
        if check_dir_exists(item_path=f'{target_path}/{item_path}'):
            pass
        else:
            print(f'\nThe dir was created {target_path}/{item_path}')
            os.makedirs(f'{target_path}/{item_path}', exist_ok=True)
            if preserve_metadata:
                os.chown(f'{target_path}/{item_path}', item_uid, item_gid)
                os.utime(f'{target_path}/{item_path}', (item_mtime, item_mtime))


def copy_file(source_item_metadata: dict, source_path: str, target_path: str, preserve_ownership: bool):
    os.makedirs(os.path.dirname(f'{target_path}/'), exist_ok=True)
    item_path = source_item_metadata['item_path']
    item_uid = source_item_metadata['uid']
    item_gid = source_item_metadata['gid']
    if source_item_metadata['type'] == 'file':
        print(f'\nThe file was copyed {source_path}/{item_path} ---> {target_path}/{item_path}')
        shutil.copy2(f'{source_path}/{item_path}', f'{target_path}/{item_path}')
        if preserve_ownership:
            os.chown(f'{target_path}/{item_path}', item_uid, item_gid)


def change_directory_timestamp(item_metadata: dict, target_path: str):
    item_path = item_metadata['item_path']
    # item_ctime = item_metadata['ctime_unix']
    item_mtime = item_metadata['mtime_unix']
    if item_metadata['type'] == 'directory':
        # os.makedirs(os.path.dirname(f'{target_path}/'), exist_ok=True)
        print()
        print(f'The dir timestamp was changed {target_path}/{item_path}')
        print()
        os.utime(f'{target_path}/{item_path}', (item_mtime, item_mtime))         

def compare_states(left_state: dict, right_state: dict):
    to_remove = []
    to_sync = []

    for file_path, file_metadata in left_state['files'].items():
        if file_path not in right_state['files']:
            print(f'\nA new file {file_path} >>> to_sync')
        else:
            if left_state['files'][file_path] != right_state['files'][file_path]:
                # print(left_state['files'][file_path])
                print(f'\nA changed file {file_path} >>> to_sync')

    for file_path, file_metadata in right_state['files'].items():
        if file_path not in left_state['files']:
            print(f'\nA removed file {file_path} >>> to_remove')

