# python-backup-tool

## Plan

1. Gather metadata from source and target folders. +

2. The target directory structure will be created +

2.1 Create function that compares `left` (source) and `right` (destination) metadata.
    It should compare `current` <> `previous`.
    It should compare `current` <> `target`.
    return dict with:
        - changed or added files ( copy to target )
        - removed ( files that sould be moved to TRASH )
    >>>>>> this should replace the following steps


3. If `previous_state_file_exist` == True

3.1 Compare `current` metadata with `prevoius` metadata.
3.2 If item metadata !=  (file changed, copy file)
3.3 If metadata ==, check `target` the metadata (copy file if `current` metadata != `target`, or file is absent on target)
3.4 If no metadata in `prevoius` ( assuming the file as a new, copy to target )
3.5 Compare `previous` with `current` ( if no in `current`, assuming the file as a removed, move target file to TRASH )
3.6 End. Replace `prevoius` with `current`.

4. If `previous_state_file_exist` == False

4.1 Compare `current` metadata with `target` metadata.
4.2 If metadata != ( file was changed, copy file )
4.3 If no `target` file ( copy file was added, copy file )
4.2 Compare `target` with `current` ( if not file in `current`, assuming the file as a removed, move target file to TRASH )

## Example
```bash
python3 backup-tool.py \
    --source_path source_dir \
    --state_file backup-tool.json \
    --target_path target_dir
```