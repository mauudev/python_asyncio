import asyncio
from asyncio import Queue
from random import randrange


class Product:
    def __init__(self, product_name: str, checkout_time: float):
        self.product_name = product_name
        self.checkout_time = checkout_time


class Customer:
    def __init__(self, customer_id: int, products: list[Product]):
        self.customer_id = customer_id
        self.products = products


# consumer
async def checkout_customer(queue: Queue, cashier_number: int):
    while not queue.empty():
        customer: Customer = await queue.get()
        print(
            f"The Cashier_{cashier_number} "
            f"will checkout Customer_{customer.customer_id}"
        )
        for product in customer.products:
            print(
                f"The Cashier_{cashier_number} "
                f"will checkout Customer_{customer.customer_id}'s "
                f"Product_{product.product_name}"
            )
            await asyncio.sleep(product.checkout_time)
        print(
            f"The Cashier_{cashier_number} "
            f"finished checkout Customer_{customer.customer_id}"
        )
        queue.task_done()


def generate_customer(customer_id: int) -> Customer:
    all_products = [
        Product("deer", 2),
        Product("banana", 0.5),
        Product("sausage", 0.2),
        Product("diapers", 0.2),
    ]
    products = [
        all_products[randrange(len(all_products))] for _ in range(randrange(10))
    ]
    return Customer(customer_id, products)


# producer
async def customer_generation(queue: Queue):
    customer_count = 0
    while True:
        customers = [
            generate_customer(the_id)
            for the_id in range(customer_count, customer_count + randrange(5))
        ]
        for customer in customers:
            print("Waiting to put customer in line....")
            await queue.put(customer)
            print("Customer put in line...")
        customer_count = customer_count + len(customers)
        await asyncio.sleep(0.3)


async def main():
    customer_queue = Queue(2)
    customer_producer = asyncio.create_task(customer_generation(customer_queue))
    cashiers = [checkout_customer(customer_queue, i) for i in range(3)]

    await asyncio.gather(customer_producer, *cashiers)


if __name__ == "__main__":
    asyncio.run(main())
