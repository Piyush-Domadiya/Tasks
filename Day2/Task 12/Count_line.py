#Write a program to count the number of lines in a file.
count = 0
with open("MyFile.txt", "r") as f:
    for line in f:
        count = count + 1
    
print(count)