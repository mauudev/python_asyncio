import asyncio


async def read_file(filename: str):
    with open(filename) as f:
        data: str = f.read()
    return data


async def fetch_data(data: int) -> dict:
    if data == 0:
        raise Exception("No data found ..")
    return {"data": data}


async def delayed_task(delay: int):
    await asyncio.sleep(delay)
    print("okay")


async def main():
    # raise error TiemoutError
    await asyncio.wait_for(delayed_task(delay=10), timeout=4)
    await asyncio.wait_for(delayed_task(delay=13), timeout=4)


async def main():
    try:
        async with asyncio.timeout(delay=3):
            async with asyncio.TaskGroup() as tg:
                task = tg.create_task(fetch_data(1))
                tg.create_task(fetch_data(2))
                tg.create_task(delayed_task(9))
                tg.create_task(fetch_data(0))
                tg.create_task(read_file("banana.png"))
            print(task.result())
    except* FileNotFoundError as eg:
        for error in eg.exceptions:
            print(error)
    except* TimeoutError as eg:
        for error in eg.exceptions:
            print(error)
    except* Exception as eg:
        for error in eg.exceptions:
            print(error)
    finally:
        print("Done !")


asyncio.run(main())
