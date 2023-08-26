import asyncio


class TaskGroupManager:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.task_group = None

    async def send_task(self, task):
        await self.queue.put(task)

    async def execute_tasks(self):
        while True:
            task = await self.queue.get()
            self.task_group.create_task(task.execute())

    async def run(self):
        self.task_group = asyncio.TaskGroup()
        try:
            async with self.task_group:
                await self.execute_tasks()
        except* Exception as eg:
            for error in eg.exceptions:
                print(error)


class Task:
    def __init__(self, name):
        self.name = name

    async def execute(self):
        print(f"Executing task: {self.name}")
        await asyncio.sleep(1)
        print(f"Task completed: {self.name}")


async def main():
    tg_mgr = TaskGroupManager()

    tasks = [
        Task("Task 1"),
        Task("Task 2"),
        Task("Task 3"),
    ]

    for task in tasks:
        await tg_mgr.send_task(task)

    await tg_mgr.run()


asyncio.run(main())
