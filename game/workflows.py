from datetime import timedelta
from temporalio import workflow

# Import activity, passing it through the sandbox without reloading the module
with workflow.unsafe.imports_passed_through():
    from game.activities import story_event

@workflow.defn
class StoryWorkflow:
    def __init__(self):
        self._players = []
        
    @workflow.run
    async def run(self) -> str:
        await workflow.wait_condition(lambda: len(self._players) > 0)
        
        await workflow.execute_activity(
            story_event, "You make some progress!", start_to_close_timeout=timedelta(seconds=5)
        )
        
        await workflow.execute_activity(
            story_event, "You get ahead to ahead with a goblin!", start_to_close_timeout=timedelta(seconds=5)
        )        

    @workflow.signal
    def add_player(self, player_name: str) -> None:
        self._players.append(player_name)

        

@workflow.defn
class BattleWorkflow:
    @workflow.run
    async def run(self) -> str:
        await workflow.execute_activity(
            story_event, "Battle has started!", start_to_close_timeout=timedelta(seconds=5)
        )
