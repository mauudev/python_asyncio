import asyncio


async def task(value):
    await asyncio.sleep(1)
    return value * 100


async def main():
    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(task(i)) for i in range(1, 10)]
    for t in tasks:
        print(t.result())


asyncio.run(main())
