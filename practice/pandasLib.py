
import pandas as pd
from wcwidth import center
data = {
    "Name": ["Piyush", "Rahul", "Aman"],
    "Marks": [85, 90, 78]
}

df = pd.DataFrame(data)
print("print data \n",df)
print("Mean Marks:", df["Marks"].mean())

# Basic Operations

print("Select columns \n",df["Name"]) #Select Columns
print("Filter Data \n",df[df["Marks"] > 80]) #Filter Data

df = df.drop(columns=["Grade"], errors="ignore")
df["Grade"] = ["A", "A+", "B"] #Add New Column
print("add new column \n",df)


