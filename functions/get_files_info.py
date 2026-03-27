import os


def get_files_info(working_directory, directory="."):
    """
    List the contents of a directory with file metadata.

    Args:
        working_directory: The base directory that limits the scope of operations
        directory: The relative path within working_directory to list (default: ".")

    Returns:
        A string representation of the directory contents with file sizes and types
    """
    try:
        # Get the absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Construct the full path to the target directory
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Check if target_dir falls within the working directory
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if the target is actually a directory
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # List all items in the directory
        items = os.listdir(target_dir)

        # Build the result string
        result_lines = []
        for item in sorted(items):  # Sort for consistent output
            item_path = os.path.join(target_dir, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            result_lines.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(result_lines)

    except Exception as e:
        return f"Error: {str(e)}"
