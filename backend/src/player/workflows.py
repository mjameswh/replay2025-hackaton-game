import typing

import models
from temporalio import workflow


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
        pass

    @workflow.signal
    async def event_from_player(self, event: str):
        # BattleWorkflow.send_signal()
        pass
