my_list = ["I", "love", "marmite"]
print(my_list[2])

my_list.append("crumpets")
print(my_list)

list.reverse(my_list)
print(my_list)

print(len(my_list))

#create a variable that holds a list of three words
words = ['First', 'Second', 'Third']
#print each of those words in turn 
for word in words: 
    #everything in the indented block is run for each of the 3 elements in the list 
    print(word)  
    
print(list(range(10)))

#loop through a list 0-2
for i in range (3): 
    print(i)
for i in range(3):
    print (i, words[i])

# here is your list of numbers
numbers = [1,2,3,4,5,6,7,8,9,10,15,30]

# this variable will hold your result, start it at 0
total = 0

# MISSING LINE HERE
# loop through the list
for i in range(len(numbers)):
    
	# INCOMPLETE LINE HERE
	# add each number to the total
	total += numbers[i]

# print the result
print(total)
