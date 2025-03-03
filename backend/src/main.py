"""Echo server using the asyncio API."""

import asyncio

from battle.workflows import BattleWorkflow
from temporalio.client import Client
from temporalio.worker import Worker
from websockets.asyncio.server import serve


async def receive_message(websocket):
    async for message in websocket:
        await websocket.send(message)


async def run_temporal_worker():
    client = await Client.connect("localhost:7233", namespace="default")
    worker = Worker(
        client,
        task_queue="hello-task-queue",
        workflows=[BattleWorkflow],
        activities=[],
    )

    await worker.run()


async def run_webserver():
    async with serve(receive_message, "localhost", 8765) as server:
        await server.serve_forever()


async def main():
    run_futures = [
        run_temporal_worker(),
        run_webserver(),
    ]

    await asyncio.gather(*run_futures)


if __name__ == "__main__":
    asyncio.run(main())
