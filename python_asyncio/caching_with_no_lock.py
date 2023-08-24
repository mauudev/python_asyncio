import asyncio

import aiohttp

cache = dict()


async def request_remote():
    print("Will request the website to get status.")
    async with aiohttp.ClientSession() as session:
        response = await session.get("https://www.example.com")
        return response.status


async def get_value(key: str):
    if key not in cache:
        print(f"The value of key {key} is not in cache.")
        value = await request_remote()
        cache[key] = value
    else:
        print(f"The value of key {key} is already in cache.")
        value = cache[key]
    print(f"The value of {key} is {value}")
    return value


async def main():
    task_one = asyncio.create_task(get_value("status"))
    task_two = asyncio.create_task(get_value("status"))

    await asyncio.gather(task_one, task_two)


if __name__ == "__main__":
    asyncio.run(main())
