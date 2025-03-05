from datetime import timedelta

from temporalio import workflow

from models import BattleState

# Import activity, passing it through the sandbox without reloading the module
with workflow.unsafe.imports_passed_through():
    from story.activities import story_event


@workflow.defn
class StoryWorkflow:
    def __init__(self):
        self._players = []

    @workflow.run
    async def run(self) -> str:
        await workflow.wait_condition(lambda: len(self._players) > 0)

        await workflow.execute_activity(
            story_event,
            "You make some progress!",
            start_to_close_timeout=timedelta(seconds=5),
        )

        await workflow.execute_activity(
            story_event,
            "You get head to head with a goblin! Prepare for battle!",
            start_to_close_timeout=timedelta(seconds=5),
        )

        await workflow.execute_child_workflow(
            BattleWorkflow.run,
            BattleState(players=self._players),
            id="battle1",
        )

        await workflow.execute_activity(
            story_event,
            "Battle has ended!",
            start_to_close_timeout=timedelta(seconds=5),
        )


    @workflow.signal
    def add_player(self, player_name: str) -> None:
        self._players.append(player_name)


@workflow.defn
class BattleWorkflow:
    """
    Run: start the battle, establish turn order, and signal the first player
    """

    @workflow.init
    def __init__(self):
        pass

    @workflow.run
    async def run(self) -> str:
        await workflow.execute_activity(
            story_event,
            "Battle has started!",
            start_to_close_timeout=timedelta(seconds=5),
        )

    @workflow.signal
    async def take_turn(self, turn: str) -> None:
        """
        ParticipantWorkflows signal their turn.

        In a future version, the ParticipantWorkflow identifies which other Participant they want to attack.
        """
        pass
