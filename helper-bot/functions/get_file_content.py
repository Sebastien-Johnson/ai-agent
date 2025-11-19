import os
from config import CHAR_LIMIT

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(CHAR_LIMIT)
            if os.path.getsize(abs_file_path) >= CHAR_LIMIT:
                file_content_string += (
                    f'[...File "{file_path}" truncated at {CHAR_LIMIT} characters]'
                )
        return file_content_string
    except Exception as e:
        return f"Error reading {file_path}: {e}"