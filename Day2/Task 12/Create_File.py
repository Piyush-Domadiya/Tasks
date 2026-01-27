#Write a program to create a text file and write some content to it.
f = open("MyFile.txt", "a")
with open("MyFile.txt", "w") as f:
    f.write("Hello,\n Python! \n")
    f.write("How are you? \n")
    f.write("this is a sample text file.")

f.close()