import asyncio

from run_worker import SayHello
from temporalio.client import Client


async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")

    # Execute a workflow
    result = await client.execute_workflow(
        SayHello.run, "Temporal", id="hello-workflow", task_queue="hello-task-queue"
    )

    print(f"Result: {result}")


asyncio.run(main())