import asyncio
from asyncio import Condition


async def do_work(condition: Condition):
    print("do_work: Acquiring condition lock...")
    async with condition:
        print("do_work: Acquired lock, release and waiting for notify...")
        await condition.wait()
        print("do_work: Condition notified, re-acquire and do work.")
        await asyncio.sleep(1)
        print("do_work: Finished work, release condition lock.")


async def fire_event(condition: Condition):
    await asyncio.sleep(5)
    print("fire_event: Acquiring condition lock....")
    async with condition:
        print("fire_event: Acquired lock, notify all workers.")
        condition.notify_all()
        print("fire_event: Notify finished, release the work...")


async def main():
    condition = Condition()
    asyncio.create_task(fire_event(condition))

    await asyncio.gather(do_work(condition), do_work(condition))


if __name__ == "__main__":
    asyncio.run(main())
