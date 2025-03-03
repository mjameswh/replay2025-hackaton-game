"""Echo server using the asyncio API."""

import asyncio

from battle.workflows import BattleWorkflow
from player.workflows import PlayerWorkflow
from npc.workflows import NpcWorkflow
from temporalio.client import Client
from temporalio.worker import Worker
from websockets.asyncio.server import serve

active_connections = {}

client = Client.connect("localhost:7233", namespace="default")
handle = None

async def receive_message(websocket):
    global client, handle
    async for message in websocket:
        if handle is None:
            handle = await client.start_workflow(PlayerWorkflow.run, "my name", id="my-workflow-id", task_queue="my-task-queue")
        await handle.signal(PlayerWorkflow.event_from_player, message)


async def run_temporal_worker():
    global client
    worker = Worker(
        client,
        task_queue="hello-task-queue",
        workflows=[BattleWorkflow, NpcWorkflow, PlayerWorkflow],
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
