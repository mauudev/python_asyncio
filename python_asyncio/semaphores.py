import asyncio
from asyncio import Semaphore

from aiohttp import ClientSession

# Evitar a toda costa llamar implicitamente semaphore.release
# descuenta el contador interno y se producen errores extranios
# que pueden ocasionar race conditions. Usar siempre como async context manager


async def get_url(url: str, session: ClientSession, semaphore: Semaphore):
    print("Waiting to acquire semaphore...")
    async with semaphore:
        print("Semaphore acquired, requesting...")
        response = await session.get(url)
        print("Finishing requesting")
        return response.status


async def main():
    # Although we start 1000 tasks, only 10 tasks will be executed at the same time.
    semaphore: Semaphore = Semaphore(10)
    async with ClientSession() as session:
        tasks = [
            asyncio.create_task(get_url("https://www.example.com", session, semaphore))
            for _ in range(1000)
        ]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
