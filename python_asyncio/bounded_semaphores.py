import asyncio
from asyncio import BoundedSemaphore

# La idea de esto es evitar el decrement interno del counter
# asi evitamos ejecutar tareas extras por encima del limite (2)
# como ocurre en Semaphore tradicional.


async def main():
    semaphore = BoundedSemaphore(2)

    await semaphore.acquire()
    semaphore.release()
    semaphore.release()


if __name__ == "__main__":
    asyncio.run(main())
