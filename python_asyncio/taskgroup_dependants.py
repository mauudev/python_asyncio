import asyncio


async def task1():
    print("Starting Task 1")
    await asyncio.sleep(2)
    print("Task 1 Done")
    return "Result from Task 1"


async def task2(result_from_task1):
    print("Starting Task 2")
    await asyncio.sleep(1)
    print("Task 2 Done with result:", result_from_task1)


async def main():
    async with asyncio.TaskGroup() as tg:
        result = await tg.create_task(task1())
        await tg.create_task(task2(result))


asyncio.run(main())
