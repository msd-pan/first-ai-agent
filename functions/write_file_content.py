import os


def write_file(working_directory, file_path, content):
    """
    Write content to a file within the working directory.

    Args:
        working_directory: The base directory that limits the scope of operations
        file_path: The relative path to the file within working_directory
        content: The string content to write to the file

    Returns:
        A string indicating success or describing any error
    """
    try:
        # Get the absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Construct the full path to the target file
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Check if target_file falls within the working directory
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Check if the target path is an existing directory
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Create parent directories if they don't exist
        parent_dir = os.path.dirname(target_file)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        # Write the content to the file
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}"
