import os
import hashlib
import sys
import time

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

    start_time = time.time()

    file_dict, duplicate_list = scan_files(path, detail=7)

    for dupe in duplicate_list:
        print(f"Duplicate files found for {dupe}:")
        for file in file_dict[dupe]:
            print(f"  {file['name']}")

    end_time = time.time()
    run_time = end_time - start_time
    sys.stderr.write(f"\nTotal run time: {run_time} seconds\n")

    print("\nDone.\n")


def scan_files(path, detail=0):
    duplicate_list = {}
    file_dict = {}

    count = 0

    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            count += 1
            if detail > 0 and count % detail == 0:
                sys.stderr.write(f"\rProcessed {count} files...")

            try:
                file_size = os.path.getsize(file_path)

                # Skip empty files
                if file_size == 0:
                    continue

                # Report large files
                if file_size > 1024 * 1024 * 1024:
                    sys.stderr.write(
                        f"\r\nProcessing large file: {file_path}, size: {file_size}\n"
                    )
                    start_time = time.time()

                file_hash = get_md5_hash(file_path)

                if file_size > 1024 * 1024 * 1024:
                    end_time = time.time()
                    run_time = end_time - start_time
                    sys.stderr.write(
                        f"Time taken to calculate MD5 hash for {file_path}: {run_time} seconds\n"
                    )

                key = f"{file_size}:{file_hash}"
                file_info = {
                    "name": file_path,
                    "size": file_size,
                    "md5_hash": file_hash,
                    "key": key,
                }

                if key in file_dict:
                    file_dict[key].append(file_info)
                    duplicate_list[key] = key
                else:
                    file_dict[key] = [file_info]
            except Exception as e:
                sys.stderr.write(f"\r\nError processing file: {file_path}\n")
                sys.stderr.write(f"Exception: {str(e)}\n")
                continue

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
