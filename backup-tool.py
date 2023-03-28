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
    
    target_path = args.target_path
    target_path_files = []
    current_target_state_body = []

    current_source_state_body = utils.generate_dir_metadata(dir_path=source_path, return_absolute_paths=True)
    current_target_state_body = utils.generate_dir_metadata(dir_path=target_path, return_absolute_paths=True)

    previous_state_file_exist = utils.check_file_exists(file_path=state_file)

    # source_path_files = utils.get_nested_files(directory=source_path)

    # current_source_state_body = utils.generate_dir_metadata(dir_path=source_path)

    # utils.copy_files(source_dir_metadata=current_source_state_body, 
    #                 source_path=source_path, 
    #                 target_path=target_path,
    #                 preserve_ownership=True)

    # current_target_state_body = utils.generate_dir_metadata(dir_path=target_path)

    # if previous_state_file_exist:
    #     previous_state_body = utils.import_json(json_file_path=state_file)
    #     # print(previous_state_body)

    #     for path in source_path_files:
    #         current_file_metadata = {}
    #         previous_file_metadata = {}
    #         target_file_metadata = {}
    #         target_file_exists = False
    #         relative_file_path = ""
    #         relative_file_path = os.path.relpath(path, source_path)
    #         # print(path)
    #         current_file_metadata = utils.generate_file_metadata(file_path=path, 
    #                                                              dir_path=source_path)
    #         print()
    #         print('Request current_file_metadata')
    #         print(f'{path}')
    #         previous_file_metadata = utils.get_file_metadata_from_state(state=previous_state_body, 
    #                                                                     file_path=relative_file_path)
    #         target_file_exists = utils.check_file_exists(file_path=f'{target_path}/{relative_file_path}')

    #         if target_file_exists:
    #             if current_file_metadata != previous_file_metadata:
    #                 print('File changed')
    #                 print('current_file_metadata:')
    #                 print(current_file_metadata)
    #                 print('previous_file_metadata:')
    #                 print(previous_file_metadata)
    #                 utils.copy_file(source_path=f'{source_path}/{relative_file_path}',
    #                                 source_metadata=current_file_metadata,
    #                                 target_path=f'{target_path}/{relative_file_path}',
    #                                 preserve_ownership=True)
    #             else:
    #                 target_file_metadata = utils.generate_file_metadata(file_path=f'{target_path}/{relative_file_path}', 
    #                                                                     dir_path=target_path)
    #                 # print()
    #                 # print('Request target_file_metadata')
    #                 # print(f'{target_path}/{relative_file_path}')
    #                 if current_file_metadata != target_file_metadata:
    #                     print('File changed')
    #                     print('current_file_metadata:')
    #                     print(current_file_metadata)
    #                     print('target_file_metadata:')
    #                     print(target_file_metadata)
    #         else:
    #             utils.copy_file(source_path=f'{source_path}/{relative_file_path}',
    #                             source_metadata=current_file_metadata,
    #                             target_path=f'{target_path}/{relative_file_path}',
    #                             preserve_ownership=True)         





    # print(f'File `{state_file}` exists' if previous_state_file_exist else f'File `{state_file}` doesnt exist and will be created')
    
    

    # utils.copy_files(source_dir_metadata=current_source_state_body, 
    #                 source_path=source_path, 
    #                 target_path=target_path,
    #                 preserve_ownership=True)


    utils.export_json(json_file_path='debug/source_state.json', 
                      body=current_source_state_body)                  
    utils.export_json(json_file_path='debug/target_state.json', 
                      body=current_target_state_body)

    print(f'Source items: {len(current_source_state_body)}')
    
        

    # utils.export_json(json_file_path='target_state.json', body=target_current_source_state_body)


if __name__ == '__main__':
    main()