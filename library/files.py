import os

# Return files from path
def find_files(path, filt):
    if not os.path.exists(path):
        return []

    files = []
    for file in os.listdir(path):
        file_path = os.path.join(path,file)
        if os.path.isfile(file_path):
            if filt in file:
                files.append(file_path)
        else:
            if not ".git" in file:
                files.extend(find_files(file_path, filt))

    return files
