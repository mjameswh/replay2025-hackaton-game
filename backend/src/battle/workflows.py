from dataclasses import dataclass

from models import UserState
from temporalio import workflow


@dataclass
class BattleState:
    players: list[UserState]  # ordered in turn order
    current_player_index: int


@workflow.defn
class BattleWorkflow:
    @workflow.init
    @workflow.run
    async def run(self, state: BattleState) -> str:
        self.state = state
        while True:
            if self.should_continue_as_new():
                await workflow.wait_condition(lambda: workflow.all_handlers_finished())
                workflow.continue_as_new(state)
