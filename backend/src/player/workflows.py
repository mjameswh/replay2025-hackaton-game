from datetime import timedelta
from temporalio import workflow

import models
import typing

@workflow.defn
class PlayerWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        pass
    
    @workflow.signal
    async def update_history(self, history: typing.List[models.Action]):
        self.history = history

        # TODO: send to the player with websockets new events

    
    @workflow.signal
    async def your_move_event(self):
        # TODO: send an event with websocket