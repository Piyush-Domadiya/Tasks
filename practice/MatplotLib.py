import matplotlib.pyplot as plt
x = [1, 2, 3, 4]
y = [10, 20, 25, 30]

#Line Chart Example
plt.plot(x, y)
plt.title("Simple Line Chart")
plt.xlabel("X Values")
plt.ylabel("Y Values")
plt.show()

#Bar Chart Example
names = ["A", "B", "C"]
marks = [80, 90, 75]

plt.bar(names, marks)
plt.title("Marks Chart")
plt.show()

#Pie Chart Example
sizes = [40, 30, 20, 10]
labels = ["Python", "Java", "C++", "JS"]

plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.show()

#Scatter Plot
x = [1,2,3,4,5]
y = [5,7,6,8,7]

plt.scatter(x, y)
plt.show()
