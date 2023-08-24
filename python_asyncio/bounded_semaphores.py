import asyncio
from asyncio import BoundedSemaphore


async def main():
    semaphore = BoundedSemaphore(2)

    await semaphore.acquire()
    semaphore.release()
    semaphore.release()


if __name__ == "__main__":
    asyncio.run(main())
