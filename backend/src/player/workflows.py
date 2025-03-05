from dataclasses import dataclass
import typing

import models
from temporalio import workflow

@dataclass
class PlayerWorkflowInput:
    name: str
    session_token: str
    host_id: typing.Optional[str] = None

@dataclass
class PlayerConnectToHostInput:
    host_id: str

@dataclass
class PlayerDisconnectFromHostInput:
    host_id: str


@dataclass
class PlayerEventFromPlayerInput:
    message: str

@workflow.defn
class PlayerWorkflow:
    def __init__(self):
        self.name: str
        self.session_token: str
        self.host_id: typing.Optional[str] = None

    @workflow.run
    async def run(self, input: PlayerWorkflowInput) -> None:
        self.name = input.name
        self.session_token = input.session_token

        while True:
            await workflow.wait_condition(workflow.info().is_continue_as_new_suggested)
            await workflow.wait_condition(workflow.all_handlers_finished)
            workflow.continue_as_new((PlayerWorkflowInput(
                name=self.name,
                session_token=self.session_token,
                host_id=self.host_id,
            )))


    @workflow.signal
    async def connect_to_host(self, args: PlayerConnectToHostInput):
        self.host_id = args.host_id


    @workflow.signal
    async def disconnect_from_host(self, args: PlayerDisconnectFromHostInput):
        # Receiving the `host_id` here prevents a race condition where the
        # workflow may have already received a new `connect_to_host` signal.
        if self.host_id == args.host_id:
            self.host_id = None


    @workflow.signal
    async def update_history(self, history: typing.List[models.Action]):
        self.history = history

        # TODO: send to the player with websockets new events

    @workflow.signal
    async def update_history(self, history: typing.List[models.Action]):
        self.history = history

        # TODO: send to the player with websockets new events

    @workflow.signal
    async def your_move_event(self):
        # TODO: send an event with websocket
        pass

    @workflow.signal
    async def event_from_player(self, event: PlayerEventFromPlayerInput):
        workflow.logger.error(f"Received event from player: {event}")
        # BattleWorkflow.send_signal()
        pass
