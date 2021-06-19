import glob
import random
import os
import shutil

def get_csv_files() -> list:
    folders:list = glob.glob("../data/VIDEO/*")
    csv:list = []
    for folder in folders:
        for file in glob.glob(folder + "/*.csv"):
            csv.append(file)
    random.shuffle(csv)
    return csv

def create_folders() -> None:
    folders:list = ["../data/train_set", "../data/val_set", "../data/test_set"]
    for folder in folders:
        try:
            shutil.rmtree(folder)
            os.rmdir(folder)
        except:
            pass
        os.mkdir(folder)

def create_sets(csv:list, size:int) -> None:
    train_size:int = int(size * 0.68)
    test_size:int = int((size - train_size) * 0.6)
    val_test:int = size - train_size - test_size
    folders:list = [["../data/train_set/", train_size], ["../data/test_set/", test_size], ["../data/val_set/", val_test]]
    pointer_csv:int = 0
    for folder, size in folders:
        while size > 0:
            shutil.copyfile(csv[pointer_csv], folder + csv[pointer_csv].split("/")[-1])
            pointer_csv += 1
            size -= 1

def main() -> None:
    csv:list = get_csv_files()
    size:int = len(csv)
    create_folders()
    create_sets(csv, size)

if __name__ == "__main__":
    main()