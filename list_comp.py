list=[10,17,20,30,21,40,50]
list1=[x for x in list if x==50 ] 
print(list1)
x=5
result="Even" if x%2==0 else "odd"
print(result)

# Original list
numbers = [5,10,20,30,40,50]
# List comprehension: [x//2 for x in list]
result1 = [x//5 for x in numbers] 
print(result1)  # 1,2,4,6,8,10

# List comprehension: [x for x in list if x//2]
result2 = [x for x in numbers if x//5]
print(result2)  # 5,10,20,30,40,50   
