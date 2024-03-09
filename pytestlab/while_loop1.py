"""
def odd_numbers(maximum):
    
    return_string = "" # Initializes variable as a string
    if maximum == 1 or maximum == 3:
        maximum += 1
    # Complete the for loop with a range that includes all 
    # odd numbers up to and including the "maximum" value.
    for i in range(1,maximum,2): 

        # Complete the body of the loop by appending the odd number
        # followed by a space to the "return_string" variable.
        return_string += str(i) + " "         

    # This .strip command will remove the final " " space 
    # at the end of the "return_string".
    return return_string.strip()


print(odd_numbers(6))  # Should be 1 3 5
print(odd_numbers(10)) # Should be 1 3 5 7 9
print(odd_numbers(1))  # Should be 1
print(odd_numbers(3))  # Should be 1 3
print(odd_numbers(0))  # No numbers displayed

print('##########\n')

def counter(start, stop):
    if start > stop:
        stop_point = stop
        return_string = "Counting down: "
        while start >= stop_point: # Complete the while loop
            return_string += str(start) # Add the numbers to the "return_string"
            if start > stop:
                return_string += ","
            start -= 1 # Increment the appropriate variable
    else:
        stop_point = start
        return_string = "Counting up: "
        while start <= stop:  # Complete the while loop
            return_string += str(start) # Add the numbers to the "return_string"
            if start < stop:
                return_string += ","
            start += 1 # Increment the appropriate variable
    return return_string


print(counter(1, 10)) # Should be "Counting up: 1,2,3,4,5,6,7,8,9,10"
print(counter(2, 1)) # Should be "Counting down: 2,1"
print(counter(5, 5)) # Should be "Counting up: 5"

print('##########\n')

def sequence(low, high):
    # Complete the outer loop range to make the loop run twice
    # to create two rows
    for x in range(1,high,1): 
        # Complete the inner loop range to print the given variable
        # numbers starting from "high" to "low" 
        # Hint: To decrement a range parameter, use negative numbers
        for y in range(high,0,-1): 
            if y == low:
                # Don’t print a comma after the last item
                print(str(y)) 
            else:
                # Print a comma and a space between numbers
                print(str(y), end=", ") 

sequence(1, 3)

print('##########\n')

for number in range(2,13,2):
    print(number)

# Should print:
# 2
# 4
# 6
# 8
# 10
# 12

print('##########\n')    

number = 1 # Initialize the variable
while number <= 7: # Complete the while loop condition
    print(number, end=" ")
    number += 1 # Increment the variable

# Should print 1 2 3 4 5 6 7    

print('##########\n')
for sum in range(5):
    sum += sum
    print(sum)

print('________\n')

def count_numbers(first, last):
  x = first
  while x <= last:
    print(x)
    x += 1

count_numbers(2, 6)

"""
"""
# below is wrong
def even_numbers(n):
    count = 0
    current_number = n
    while count <= current_number: # Complete the while loop condition
        if current_number % 2 == 0:
            count +=1 # Increment the appropriate variable
            # Increment the appropriate variable
    return count
"""
"""
def even_numbers(n):
    count = 0
    current_number = n
    result = 0
    A = 10
    while count <= (current_number): # Complete the while loop condition
        count += 1
        #if current_number % 2 == 0:
        result = current_number // 2 
        return(result+1)
    #return result
    
print(even_numbers(25))   # Should print 13
"""
def even_numbers(n):
    count = 0
    current_number = n
    result = 0
    while count <= (current_number): # Complete the while loop condition
        count += 1
        if current_number % 2 == 0:
           result = current_number // 2 
    return(result+1)
    
    
print(even_numbers(25))   # Should print 13
print(even_numbers(144))  # Should print 73
print(even_numbers(1000)) # Should print 501
print(even_numbers(0))    # Should print 1