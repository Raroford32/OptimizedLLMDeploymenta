import os

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)

def read_file(path):
    with open(path, 'r') as f:
        return f.read()
