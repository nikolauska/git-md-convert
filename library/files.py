import os

# Return files from path
def find_files(path, filt, start=os.curdir):
    if not os.path.exists(path):
        return []

    files = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            if filt in file:
                files.append(os.path.relpath(file_path, start=start))
        else:
            if not ".git" in file:
                files.extend(find_files(file_path, filt, start=start))

    return files

def generate_folders(path):
    (head, tail) = os.path.split(path)
    if not os.path.exists(head):
        os.makedirs(head)
