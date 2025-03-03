import asyncio

from game.workflows import StoryWorkflow
from temporalio.client import Client
import random


async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")

    # Execute a workflow
    id = "hello-workflow-"+str(random.randint(1, 100000000))
    
    result = await client.start_workflow(
        StoryWorkflow.run, id=id, task_queue="default"
    )

    print(f"Result: {result}")


asyncio.run(main())