#list1 = [1, 2, 3, 4, 5]
#list2 = [6, 7, 8, 9, 10]

#if len(list1) > len(list2):
#    print("List1 大於 List2")
#elif len(list1) < len(list2):
#    print("List1 小於 List2")
#else:
#    print("List1 等於 List2")



#list1 = [1, 2, 3, 4, 5]
#list2 = [6, 7, 8, 9, 10]

# 假設列表的元素都是數值
#if sum(list1) > sum(list2):
#    print("List1 的元素總和大於 List2")
#elif sum(list1) < sum(list2):
#    print("List1 的元素總和小於 List2")
#else:
#    print("List1 的元素總和等於 List2")

#my_list = [1, 2, 2, 3, 4, 4, 5]

#for i in my_list:
#    print(my_list.count(i))

# 將列表轉換為集合，去除重複值
#unique_set = set(my_list)
#print(f'{unique_set}\n')
# 找出重複值
#duplicates = [item for item in unique_set if my_list.count(item) > 1]

#print("重複值:", duplicates)

#my_list = [1, 2, 2, 3, 4, 4, 5]

# 找出重複值
#duplicates = []
#for item in my_list:
#    if my_list.count(item) > 1 and item not in duplicates:
#        duplicates.append(item)
#print("重複值:", duplicates)


#fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
#newlist = []

#for x in fruits:
#  if "a" in x:
#    newlist.append(x)
#print(newlist)

#fruits = ["apple", "banana", "cherry", "kiwi", "mango"]

#newlist = [x for x in fruits if "a" in x]

#print(newlist)

#You can use the range() function to create an iterable:

#newlist = [x for x in range(10)]
#print(newlist)

#fruits = ["apple", "banana", "cherry", "kiwi", "mango"]

#newlist = [x.upper() for x in fruits]

#print(newlist)

#fruits = ["apple", "banana", "cherry", "kiwi", "mango"]

#newlist = ['hello' for x in fruits]

#print(newlist)

#fruits = ["apple", "banana", "cherry", "kiwi", "mango"]

#newlist = [x if x != "banana" else "orange" for x in fruits]

#print(newlist)

#thislist = [100, 50, 65, 82, 23]
#thislist.sort()
#print(thislist) 

"""
my_list = [77, 77, 1, 2, 2, 3, 4, 4, 5, 'FF', "123", "FF",0XAF,0XAB,0XAF]
duplicates = []

for item in my_list:
    if my_list.count(item) > 1 and item not in duplicates:
        duplicates.append(item)

print("重複值:", duplicates)

# 將所有元素轉換成字符串後再進行排序
duplicates = [str(item) for item in duplicates]
duplicates.sort()

print("排序後的重複值:", duplicates)
"""

def myfunc(n):
  return abs(n - 50)

thislist = [100, 50, 65, 82, 23]

thislist.sort(key = myfunc)

print(thislist)





