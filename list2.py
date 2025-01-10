# def rebind_and_modify(lst):
#     lst = [5, 6, 7]  # This creates a new list and rebinds lst locally
#     lst.append(8)     # Modify the new list
#     return lst        # Return the new list reference

# my_list = [1, 2, 3]  # Original list
# my_list = rebind_and_modify(my_list)  # Rebind my_list to the returned list


# def rebind_list(lst):
#     lst = [7, 8, 9]  
#     print("list inside funtion ",lst)

# my_list = [1, 2, 3]  
# result=rebind_list(my_list)  
# print(my_list)

# def rebind_list(lst=[50, 60]):  # Default argument with a mutable list
#     lst.append(10)  # Modify the list in place
#     print(lst)

# my_list = [1, 2, 3]  # Original list
# result = rebind_list(my_list)  # Pass my_list to the function
# print(my_list)  # Print the original list after the function call


check1 = ['Learn', 'Quiz', 'Practice', 'Contribute'] 
check2 = check1 
check3 = check1[:] 

check2[0] = 'Code'
check3[1] = 'Mcq'

count = 0
for c in (check1, check2, check3): 
	if c[0] == 'Code': 
		count += 1
	if c[1] == 'Mcq': 
		count += 10

print (count) 
