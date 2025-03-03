from models import UserState
from temporalio import workflow


@workflow.defn
class BattleWorkflow:
    @workflow.run
    async def run(self, state: BattleState) -> str:
        self.state = state
        while True:
            if self.should_continue_as_new():
                await workflow.wait_condition(lambda: workflow.all_handlers_finished())
                workflow.continue_as_new(state)

    @workflow.signal
    async def start_battle(self, players: list[UserState]) -> None:
        self.state.players = players
        self.state.current_player_index = 0
