import asyncio
from asyncio import Semaphore

# Sometimes, due to code limitations, we can’t use async with to manage the acquire
# and release of semaphore locks, so we might call acquire somewhere and release somewhere else.
# What happens if we accidentally call the asyncio.Semaphore release method multiple times?

# As the code shows, we are limited to running two tasks simultaneously,
# but because we called release more than once, we can run three tasks at the same time next time.
# To solve this problem, we can use asyncio.BoundedSemaphore .


async def acquire(semaphore: Semaphore):
    print("acquire: Waiting to acquire...")
    async with semaphore:
        print("acquire: Acquired...")
        await asyncio.sleep(5)
    print("acquire: Release...")


async def release(semaphore: Semaphore):
    print("release: Releasing as one off...")
    semaphore.release()
    print("release: Released as one off...")


async def main():
    semaphore = Semaphore(2)

    await asyncio.gather(
        asyncio.create_task(acquire(semaphore)),
        asyncio.create_task(acquire(semaphore)),
        asyncio.create_task(
            release(semaphore)
        ),  # release del context manager + release extra
    )

    await asyncio.gather(
        asyncio.create_task(acquire(semaphore)),
        asyncio.create_task(acquire(semaphore)),
        asyncio.create_task(acquire(semaphore)),
    )


if __name__ == "__main__":
    asyncio.run(main())
