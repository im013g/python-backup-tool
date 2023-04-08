#!/usr/bin/env python3

import argparse
import utils
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_path', help='', required=True)
    parser.add_argument('--state_file', help='', required=True)
    parser.add_argument('--target_path', help='', required=True)
    # parser.add_argument('--target_state_file', help='', required=True)
    args = parser.parse_args()

    source_path = args.source_path
    source_path_files = []
    current_source_state_body = []
    previous_state_file_exist = bool
    previous_state_body = []
    state_file = args.state_file
    create_new_state_file = bool
    
    target_path = args.target_path
    target_path_files = []
    current_target_state_body = []

    '''
    Metadata will be collected from both the source and target directories
    '''
    current_source_state_body = utils.generate_dir_metadata(dir_path=source_path, return_absolute_paths=True)
    current_target_state_body = utils.generate_dir_metadata(dir_path=target_path, return_absolute_paths=True)

    previous_state_file_exist = utils.check_file_exists(item_path=state_file)

    """
    The target directory structure will be created
    """
    for current_item_metadata in reversed(current_source_state_body):
        if current_item_metadata['type'] == 'directory':
            utils.copy_directory(source_item_metadata=current_item_metadata,
                                target_path=target_path,
                                preserve_metadata=False)


    if previous_state_file_exist:
        previous_state_body = utils.import_json(json_item_path=state_file)

        for current_item_metadata in current_source_state_body:
            if current_item_metadata['type'] == 'file':
                previous_item_metadata = {}
                target_item_metadata = {}

                previous_item_metadata = utils.get_file_metadata_from_state(file_metadata=current_item_metadata, state_body=previous_state_body)

                if current_item_metadata != previous_item_metadata:
                    """
                    File was changed or created.
                    """
                    # print(f'''File was changed or created {current_item_metadata['item_path']}''')
                    utils.copy_file(source_item_metadata=current_item_metadata, 
                                    source_path=source_path, 
                                    target_path=target_path, 
                                    preserve_ownership=True)
                else:
                    target_item_metadata = utils.get_file_metadata_from_state(file_metadata=current_item_metadata, state_body=current_target_state_body)
                    if  current_item_metadata != target_item_metadata:
                        utils.copy_file(source_item_metadata=current_item_metadata, 
                                        source_path=source_path, 
                                        target_path=target_path, 
                                        preserve_ownership=True)
    else:
        for current_item_metadata in current_source_state_body:
            target_item_metadata = {}                       
            target_item_metadata = utils.get_file_metadata_from_state(file_metadata=current_item_metadata, state_body=current_target_state_body)
            if  current_item_metadata != target_item_metadata:
                utils.copy_file(source_item_metadata=current_item_metadata, 
                                source_path=source_path, 
                                target_path=target_path, 
                                preserve_ownership=True)


    """
    Apply time stamp to target directories
    """
    for current_item_metadata in reversed(current_source_state_body):
        if current_item_metadata['type'] == 'directory':
            target_item_metadata = utils.get_file_metadata_from_state(file_metadata=current_item_metadata, state_body=current_target_state_body)
            if current_item_metadata != target_item_metadata:
                utils.change_directory_timestamp(item_metadata=current_item_metadata, target_path=target_path)


    "DEBUG: Get final target state body"
    current_target_state_body = utils.generate_dir_metadata(dir_path=target_path, return_absolute_paths=True)


    utils.export_json(json_item_path=state_file, 
                      body=current_source_state_body)                  
    utils.export_json(json_item_path='debug/target_state.json', 
                      body=current_target_state_body)



if __name__ == '__main__':
    print()
    main()