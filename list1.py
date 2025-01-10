def rebind_and_modify(lst):
    lst = [5, 6, 7]  # This creates a new list and rebinds lst locally
    print("inside funtion",lst)
    lst.append(8)     # Modify the new list
    return lst        # Return the new list reference

my_list = [1, 2, 3]  # Original list
print("before funtion call",my_list)
my_list = rebind_and_modify(my_list)  # Rebind my_list to the returned list
print("after funtion call",my_list)

class A:
    print("hello")

a= A()    

class B(A) :
    pass
b=B()
print(A.__bases__)

