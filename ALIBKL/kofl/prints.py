
from glob import glob

def print_file(filename):
        with open(filename, "r") as f:
                print(f.read())

def print_folder_as_options(folder):
    files = glob(folder)
    print("[0] return")
    for i in range(len(files)):
        print("[" + str(i + 1) + "] " + files[i].split("/")[-1])