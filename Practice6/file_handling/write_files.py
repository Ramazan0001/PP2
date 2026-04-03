
with open("data.txt", "w") as f:
    f.write("Hello\n")
    f.write("Python\n")
    f.write("File handling example\n")

print("File created and written successfully")

with open("data.txt" , "a" ) as file:
    file.write("NEW\n")
     
print("Data written and appended succesfully")