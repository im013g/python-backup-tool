#!/usr/bin/env python3

import argparse
import utils
import os


def get_filesystem_nested_items(directory: str, return_files: bool = True, return_dirs: bool = True, return_absolute_paths: bool = False) -> list:
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


my_list = []
my_list = get_filesystem_nested_items(directory='/Users/dswt/git/github/python-backup-tool/source_dir', 
                                      return_files=True, 
                                      return_dirs=True, 
                                      return_absolute_paths=True)

if my_list:
    for item in my_list:
        print(item)
else:
    print(my_list)