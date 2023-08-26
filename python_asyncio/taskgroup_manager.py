import asyncio
from typing import Any, Type


class TaskGroupManager:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.task_group = None

    async def append_task(self, task: Type[Any], param: Type[Any]):
        await self.queue.put(task.handle(param))

    async def create_tasks(self):
        tasks = []
        while not self.queue.empty():
            task = await self.queue.get()
            tasks.append(self.task_group.create_task(task))
            self.queue.task_done()
        return tasks

    async def execute_tasks(self):
        results = []
        self.task_group = asyncio.TaskGroup()
        async with self.task_group:
            tasks = await self.create_tasks()
        for task in tasks:
            results.append((task, task.result()))
        await self.queue.join()
        return results


class Task:
    def __init__(self, name):
        self.name = name

    async def handle(self, params):
        print(f"Executing task: {self.name} with params: {params}")
        await asyncio.sleep(1)
        print(f"Task completed: {self.name}")
        return "OK!"


async def main():
    executor = TaskGroupManager()
    tasks = [
        Task("Task 1"),
        Task("Task 2"),
    ]
    for task in tasks:
        await executor.append_task(task, "ammm")
    results = await executor.execute_tasks()
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
