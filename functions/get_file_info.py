def get_files_info(working_directory, directory="."):
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if not valid_target_dir:
        raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')