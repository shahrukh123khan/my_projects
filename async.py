import asyncio

async def async_function1():
    print("Async function 1 started")
    await asyncio.sleep(2)
    print("Async function 1 done")

async def async_function2():
    print("Async function 2 started")
    await asyncio.sleep(2)
    print("Async function 2 done")

async def async_function3():
    print("Async function 3 started")
    await asyncio.sleep(2)
    print("Async function 3 done")

async def async_function4():
    print("Async function 4 started")
    await asyncio.sleep(2)
    print("Async function 4 done")

async def async_function5():
    print("Async function 5 started")
    await asyncio.sleep(2)
    print("Async function 5 done")

async def async_function6():
    print("Async function 6 started")
    await asyncio.sleep(2)
    print("Async function 6 done")


async def main():
    # Start both asynchronous functions concurrently
    '''task1 = asyncio.create_task(async_function1())
    task2 = asyncio.create_task(async_function2())
    task3 = asyncio.create_task(async_function3())
    task4 = asyncio.create_task(async_function4())
    task5 = asyncio.create_task(async_function5())
    task6 = asyncio.create_task(async_function6())'''
     # Use asyncio.gather() to run both asynchronous functions concurrently
    print("this is main funtion 1")

    await asyncio.gather(async_function1(), async_function2())
    print("this is main funtion 2")

    '''await async_function1()                  #main courontine waiting and paused . and complete execution of funtion
    await async_function2()                     #main statment printed at same time where it is after funtion execution complete
    await async_function3()                  #main courontine waiting and paused .
    print("this is main funtion 1")

    await async_function4()
    await async_function5()                  #main courontine waiting and paused .
    await async_function6()
    print("this is main funtion")'''
 



    # Wait for both tasks to complete
    '''await task1                      #  main not waiting and partial execution of fun  main statment printed at last 
    await task2
    await task3
    print("this is main funtion 1")

    await task4
    await task5
    await task6
    print("this is main funtion")'''

asyncio.run(main())


print()
import asyncio

async def async_function1():
    print("Async function 1 started")
    await asyncio.sleep(2)
    print("Async function 1 done")

async def async_function2():
    print("Async function 2 started")
    await asyncio.sleep(2)
    print("Async function 2 done")

async def main():
    print("this is main funtion 1")
    await asyncio.gather(async_function1(), async_function2())
    print("this is main funtion 2")

asyncio.run(main())

