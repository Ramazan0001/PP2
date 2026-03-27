import os


os.makedirs("test_folder/subfolder", exist_ok=True)
print("Directories created")


print("Current directory:", os.getcwd())

print("Files and folders:")
print(os.listdir())