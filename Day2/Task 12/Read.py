#Read the content of a file and print it.
with open("MyFile.txt", "r") as f:
    contents = f.read()
    print(contents)