import os
import hashlib
import sys

"""
pyDedupe.py

A command line tool to identify deuplicate files based on 
size and md5 hash value.
"""
def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = os.getcwd()

    file_dict, duplicate_list = scan_files(path)

    for dupe in duplicate_list:
        print(f"Duplicate files found for {dupe}:")
        for file in file_dict[dupe]:
            print(f"  {file['name']}")

    print("\nDone.")

def scan_files(path):
    duplicate_list = []
    file_dict = {}

    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            file_hash = get_md5_hash(file_path)
            key = f"{file_size}:{file_hash}"
            file_info = {
                'name': file_path,
                'size': file_size,
                'md5_hash': file_hash,
                'key': key,
            }

            if key in file_dict:
                file_dict[key].append(file_info)
                duplicate_list.append(key)
            else:
                file_dict[key] = [file_info]

    return file_dict, duplicate_list

def get_md5_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    main()
