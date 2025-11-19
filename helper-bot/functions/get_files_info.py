import os

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory) #full path from workging dir
    target_dir = os.path.abspath(os.path.join(working_directory, directory)) #full path of relative directory

    if not target_dir.startswith(abs_working_dir): #checks if beginning of target dir path starts with working dir path
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir): 
        return f'Error: "{directory}" is not a directory'
    try:
        files_info = []
        for file_name in os.listdir(target_dir): #iterates through files in dir
            file_path = os.path.join(target_dir, file_name) #adds filename to relative directory path
            file_size = 0
            is_dir = os.path.isdir(file_path)
            file_size = os.path.getsize(file_path)
            files_info.append(
                f"{file_name}: file size={file_size} bytes, is_dir={is_dir} "
            )
        return "\n".join(files_info)
    except Exception as e:   
        return f"Error: {e}"
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
    