#Generate All Subsets (Backtracking)
def generate_subsets(nums):
    def backtrack(start, path):
        if not path:
            print("-")
        else:
            print("- " + " ".join(map(str, path)))

        for i in range(start, len(nums)):
            backtrack(i + 1, path + [nums[i]])

    backtrack(0, [])


input_list = list(map(int, input("Enter numbers separated by spaces: ").split()))
generate_subsets(input_list)

