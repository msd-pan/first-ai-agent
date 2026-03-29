import os
import subprocess
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file within the working directory with optional command-line arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the Python file within the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments to pass to the script",
            ),
        },
        required=["file_path"],
    ),
)


def run_python_file(working_directory, file_path, args=None):
    """
    Run a Python file within the working directory.

    Args:
        working_directory: The base directory that limits the scope of operations
        file_path: The relative path to the Python file within working_directory
        args: Optional list of command-line arguments to pass to the script

    Returns:
        A string containing the execution output or error message
    """
    try:
        # Get the absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Construct the full path to the target file
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Check if target_file falls within the working directory
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check if the file exists and is a regular file
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Check if the file is a Python file
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        # Build the command to run
        command = ["python", target_file]

        # Add additional arguments if provided
        if args:
            command.extend(args)

        # Run the subprocess
        completed_process = subprocess.run(
            command,
            cwd=working_dir_abs,  # Set working directory
            capture_output=True,   # Capture stdout and stderr
            text=True,             # Decode output to strings
            timeout=30             # 30 second timeout
        )

        # Build the output string
        output_parts = []

        # Check for non-zero exit code
        if completed_process.returncode != 0:
            output_parts.append(f"Process exited with code {completed_process.returncode}")

        # Check if any output was produced
        has_stdout = completed_process.stdout and completed_process.stdout.strip()
        has_stderr = completed_process.stderr and completed_process.stderr.strip()

        if not has_stdout and not has_stderr:
            output_parts.append("No output produced")
        else:
            # Add stdout if present
            if has_stdout:
                output_parts.append(f"STDOUT:\n{completed_process.stdout}")

            # Add stderr if present
            if has_stderr:
                output_parts.append(f"STDERR:\n{completed_process.stderr}")

        return "\n".join(output_parts)

    except subprocess.TimeoutExpired:
        return f'Error: executing Python file: execution timed out after 30 seconds'
    except Exception as e:
        return f"Error: executing Python file: {e}"
