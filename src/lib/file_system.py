import os


def read_file(file_path: str):
    file = open(file_path, "r")
    content = file.read()
    file.close()
    return content


def write_file(file_path: str, content: str):
    file = open(file_path, "w")
    _ = file.write(content)
    file.close()


def ensure_file(file_path: str, default_file_content: str = ""):
    is_file_exist = os.path.isfile(file_path)
    if not is_file_exist:
        write_file(file_path, default_file_content)
