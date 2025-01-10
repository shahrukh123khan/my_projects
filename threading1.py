# one class==one run method if we write more it will execute the last or latest one beacuase of method overriding beacuase names are same .

#-----------------class based threading-----------------------------
'''import threading
import time
class MyThread(threading.Thread):

    def run(self):    #treated as a thread 
        #time.sleep(10)
        for i in range(10):
            print("T1 ",i,end=" ")
        print("\n\n")    
   
class MyThread2(threading.Thread):

    def run(self):    #treated as a thread 
        #time.sleep(10)
        for i in range(2,10,2):
            print("T2 ",i,end=" ")
        print("\n\n")    
            
     
if __name__=="__main__":
    #time.sleep(10)
    for i in range(50,65,5):    # main thread 
        print("T 3 ",i,end=" ")
    
t1=MyThread()
#t1.my_fun()
t1.start()
t2=MyThread2()
t2.start()'''



'''import threading

def worker():
    print("Thread is working")

# Create a thread that runs the worker function
thread = threading.Thread(target=worker)
thread.start()       # Start the thread
thread.join()        # main thread or main fun will Wait for the other threads to finish and run after the completion of all the thread '''   

import threading

#---------------funtion based threading-------------------------

'''def worker():
    print("Thread is working")

thread = threading.Thread(target=worker)
thread.start()
# No thread.join() here main thread will not wait other thread 
print("Main program continues...")'''

#-------------  one funtion but two thread concept-----------------------

'''import threading
import time

def worker(thread_id):
    print(f"Thread {thread_id} is working")
    time.sleep(1)  # Simulate some work
    print(f"Thread {thread_id} has finished")

# Create two threads
thread1 = threading.Thread(target=worker, args=(1,))
thread2 = threading.Thread(target=worker, args=(2,))

# Start the threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()

print("Main program continues...")'''

#----------------------two funtion two thread concept----------------

'''def fun1():
    for i in range(10):
        print("thread1 =",i,end=" ",)
    print("\n\n")    

def fun2():
    for i in range(10,20):
        print("thread2 =",i,end=" ")
    print("\n\n")    

def fun3():
    for i in range(20,30):
        print("thread3 =",i,end=" ")
    print("\n\n")    
def fun4():
    for i in range(30,40):
        print("thread4 =",i,end=" ")
    print("\n\n")    
thread1=threading.Thread(target=fun1)
thread2=threading.Thread(target=fun2)
thread3=threading.Thread(target=fun3)
thread4=threading.Thread(target=fun4)
thread1.start()
thread2.start()
thread3.start()
thread4.start()
    
   
list=[10,20,30,40,50,60,70,80]
print("\n\n\n")
for i in list:
    print(i,end=" ")'''


#---------------------- example of thread is_alive method------------------------
# thread.is alive is used  to check thread is runing or not it retrun true or false    
#-Check Thread Status: thread.is_alive() returns True if 
#the thread is currently running, and False if it has finished execution or hasn’t started yet.

import threading
import time

def worker():
    print("Thread starting")
    time.sleep(5)
    print("Thread ending")

# Create a thread that runs the worker function
t = threading.Thread(target=worker)
t.start()

# Check if the thread is still alive after 2 seconds
time.sleep(2)
if t.is_alive():
    print("Thread is still running")

# Wait for the thread to finish
t.join()

# After joining, the thread should no longer be alive
if not t.is_alive():
    print("Thread has finished")
