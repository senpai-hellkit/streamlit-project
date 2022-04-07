import os


def get_path_to_file(file_name: str) -> str:
    return os.path.join(DATA_DIR, file_name)


WORK_DIR = os.getcwd()
DATA_DIR = os.path.join(WORK_DIR, 'data')

