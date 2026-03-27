import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    """
    Read and return the contents of a file within the working directory.

    Args:
        working_directory: The base directory that limits the scope of operations
        file_path: The relative path to the file within working_directory

    Returns:
        A string containing the file contents (up to MAX_CHARS characters)
    """
    try:
        # Get the absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Construct the full path to the target file
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Check if target_file falls within the working directory
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check if the target is actually a file (not a directory)
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read the file content
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)

            # Check if there's more content (file was truncated)
            if f.read(1):
                content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {str(e)}"
