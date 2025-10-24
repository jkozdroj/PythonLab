import os

def count_files(directory):
    file_count = 0
    directories = []
    print()
    for entry in os.listdir(directory):
        path = os.path.join(directory, entry)
        #print(f"path:{path}")
        #print(f"entry:{entry}")
        if os.path.isfile(path):
            file_count += 1
            print(path)
        elif os.path.isdir(path):
            directories.append(path)
    while directories:
       file_count += count_files(directories.pop())
    return file_count

if __name__ == "__main__":
    directory = input("Enter directory:")

    print(f"\nRecursive number of files in {directory}: {count_files(directory)}")
