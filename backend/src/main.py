"""Echo server using the asyncio API."""

import asyncio
import uuid

from story.workflows import StoryWorkflow
from story.activities import story_event
from battle.workflows import BattleWorkflow
from player.workflows import PlayerConnectToHostInput, PlayerDisconnectFromHostInput, PlayerEventFromPlayerInput, PlayerWorkflow, PlayerWorkflowInput
from npc.workflows import NpcWorkflow
from temporalio.client import Client, WorkflowHandle
from temporalio.worker import Worker
from websockets import ServerConnection
from websockets.asyncio.server import serve


active_connections = {}
client = None
host_id = uuid.uuid4()


async def main():
    run_futures = [
        run_main_temporal_worker(),
        run_host_specific_temporal_worker(),
        run_webserver(),
    ]

    await asyncio.gather(*run_futures)


async def run_main_temporal_worker():
    worker = Worker(
        await get_temporal_client(),
        task_queue="main",
        workflows=[StoryWorkflow, BattleWorkflow, NpcWorkflow, PlayerWorkflow],
        # activities=[story_event],
    )

    await worker.run()


async def run_host_specific_temporal_worker():
    worker = Worker(
        await get_temporal_client(),
        task_queue=f"host-{host_id}",
        activities=[story_event],
    )
    await worker.run()


async def run_webserver():
    async with serve(receive_message, "localhost", 8765) as server:
        await server.serve_forever()


async def get_temporal_client():
    global client
    # There is technically a race condition here that may result in two distinct
    # clients being created, but it is safe to ignore.
    if client is None:
        client = await Client.connect("localhost:7233")
    return client


async def receive_message(websocket: ServerConnection):
    session_token = websocket.request.path.split("=")[1]
    print(f"Got connection with session token {session_token}")

    global active_connections
    active_connections[session_token] = websocket

    client = await get_temporal_client()
    handle: WorkflowHandle = await client.start_workflow(
        PlayerWorkflow.run,
        PlayerWorkflowInput(name="Player Name", session_token=session_token),
        id=f"player-{session_token}",
        task_queue=f"main",
        start_signal="connect_to_host",
        start_signal_args=[PlayerConnectToHostInput(host_id=host_id)],
    )

    try:
        async for message in websocket:
            print(f"Got message {message} from session token {session_token}")
            await handle.signal(PlayerWorkflow.event_from_player, PlayerEventFromPlayerInput(message=message))
    finally:
        print(f"Closing connection with session token {session_token}")
        # FIXME:Race condition — The "disconnect" signal may be sent after the workflow has already
        # received a new "connect" signal.
        await handle.signal(PlayerWorkflow.disconnect_from_host, PlayerDisconnectFromHostInput(host_id=host_id))
        del active_connections[session_token]


if __name__ == "__main__":
    asyncio.run(main())
