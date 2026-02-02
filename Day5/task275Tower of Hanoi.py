#Tower of Hanoi (Recursive Solution)
def tower_of_hanoi(n,count, start, end, intermediate):
    if n == 1:
        count += 1
        print(f"Step {count} Move disk 1 from tower {start} to tower {end}")
        return count
    count = tower_of_hanoi(n - 1, count, start, intermediate, end)
    count += 1
    print(f"Step {count} Move disk {n} from tower {start} to tower {end}")
    count = tower_of_hanoi(n - 1, count, intermediate, end, start)
    return count
num_disks = int(input("Enter the number of disks: "))
tower_of_hanoi(num_disks, 0, 'A', 'C', 'B')  

