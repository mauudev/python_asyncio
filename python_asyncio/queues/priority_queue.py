import asyncio
from asyncio import PriorityQueue, Task
from dataclasses import dataclass, field
from enum import IntEnum
from random import randrange

from aiohttp import web
from aiohttp.web_app import Application
from aiohttp.web_request import Request
from aiohttp.web_response import Response

app = Application()
routers = web.RouteTableDef()
QUEUE_KEY = "QUEUE_KEY"
TASK_KEY = "TASK_KEY"


class UserType(IntEnum):
    POWER_USER = 1
    NORMAL_USER = 2


@dataclass(order=True)
class WorkItem:
    user_type: UserType
    order_delay: int = field(compare=False)


@routers.post("/order")
async def order(request: Request) -> Response:
    queue: PriorityQueue = app[QUEUE_KEY]
    body = await request.json()
    user_type = (
        UserType.POWER_USER if body["power_user"] == "True" else UserType.NORMAL_USER
    )
    work_item = WorkItem(user_type, randrange(5))
    await queue.put(work_item)

    return Response(body="order placed!")


async def process_order_worker(worker_id: int, queue: PriorityQueue):
    while True:
        work_item: WorkItem = await queue.get()
        print(
            f"process_order_worker: Worker_{worker_id} begin to process worker {work_item}"
        )
        await asyncio.sleep(work_item.order_delay)
        print(
            f"process_order_worker: Worker_{worker_id} finished to process worker {work_item}"
        )
        queue.task_done()


async def create_order_queue(app: Application):
    print("create_order_queue: Begin to initialize queue and tasks.")
    queue: PriorityQueue = PriorityQueue(10)
    tasks = [asyncio.create_task(process_order_worker(i, queue)) for i in range(3)]
    app[QUEUE_KEY] = queue
    app[TASK_KEY] = tasks
    print("create_order_queue: Initialize queue and tasks success..")


async def destroy_order_queue(app: Application):
    queue: PriorityQueue = app[QUEUE_KEY]
    tasks: list[Task] = app[TASK_KEY]

    try:
        print("destroy_order_queue: Wait for 20 sec to let all work done.")
        await asyncio.wait_for(queue.join(), timeout=20.0)
    except Exception as e:
        print("destroy_order_queue: Cancel all tasks.")
        [task.cancel() for task in tasks]


app.add_routes(routers)
app.on_startup.append(create_order_queue)
app.on_shutdown.append(destroy_order_queue)
web.run_app(app)
