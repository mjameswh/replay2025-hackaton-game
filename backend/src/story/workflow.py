from models import UserState
from temporalio import workflow


class StoryWorkflow:
    @workflow.signal
    async def start_battle(self, players: list[UserState]) -> None:
        await workflow.execute_child_workflow(
            BattleWorkflow.run,
            BattleWorkflowInput(players=players),
            id="battle1",
        )
