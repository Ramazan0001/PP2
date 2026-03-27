import shutil
import os


os.makedirs("test_folder", exist_ok=True)


if os.path.exists("data.txt"):
    shutil.move("data.txt", "test_folder/data.txt")
    print("File moved")
else:
    print("data.txt not found")