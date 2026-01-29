#Create a To-Do list application where users can add, edit, and delete tasks.

task=[]
def display_tasks():
    if len(task)==0:
        print("No tasks in the list.")
    else:
        print("Your To-Do List:")
        for i, t in enumerate(task, start=1):
            print(f"{i}. {t}")

def add_task():
    new_task=input("Enter the task you want to add: ")
    task.append(new_task)
    print("Task added.")

def edit_task():
    display_tasks()
    if len(task)==0:
        return
    task_num=int(input("Enter the task number you want to edit: "))
    if 1 <= task_num <= len(task):
        new_task=input("Enter the new task: ")
        task[task_num-1]=new_task
        print("Task updated.")
    else:
        print("Invalid task number.")

def delete_task():
    display_tasks()
    if len(task)==0:
        return
    task_num=int(input("Enter the task number you want to delete: "))
    if 1 <= task_num <= len(task):
        task.pop(task_num-1)
        print("Task deleted.")
    else:
        print("Invalid task number.")

while True:
    print("\nTo-Do List :")
    print("1. Display Tasks")
    print("2. Add Task")
    print("3. Edit Task")
    print("4. Delete Task")
    print("5. Exit")
    choice=input("Enter your choice (1-5): ")

    match choice:
        case '1':
            display_tasks()
        case '2':
            add_task()
        case '3':
            edit_task()
        case '4':
            delete_task()
        case '5':
            print("Exiting To-Do List application.")
            break
        case _:
            print("Invalid choice. Please enter a number between 1 and 5.")