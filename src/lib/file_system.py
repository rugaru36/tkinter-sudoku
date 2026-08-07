import os


def read_file(file_path: str):
    with open(file_path, "r") as file:
        return file.read()


def write_file(file_path: str, content: str):
    with open(file_path, "w") as file:
        _ = file.write(content)


def ensure_file(file_path: str, default_file_content: str = ""):
    is_file_exist = os.path.isfile(file_path)
    if not is_file_exist:
        write_file(file_path, default_file_content)
