#purpuse: remark "Sort by duplicating, it sorts them in ascending order."
my_list = [12, 12, 2, 32, 2, 'FF', 57, 22, 'FF', 14, 0xaf, 66, 0xaf,"FFF"]

# Define a custom sorting key function
def custom_sort(item):
    if isinstance(item, int):
        return 0, item  # Sort integers first
    else:
        return 1, item  # Sort other types after integers

# Sort the list using the custom key
sorted_list = sorted(my_list, key=custom_sort)

print(sorted_list)
