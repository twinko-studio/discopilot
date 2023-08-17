import asyncio

async def foo():
    return 42

async def bar():
    result = await foo()
    print(result)

asyncio.run(bar())

async def main():
    task1 = asyncio.create_task(foo())
    task2 = asyncio.create_task(bar())
    
    await task1
    await task2


