import os
if os.path.exists("MyFile1.txt"):
  os.remove("MyFile1.txt")
else:
  print("The file does not exist")