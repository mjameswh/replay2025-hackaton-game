from dataclasses import dataclass
from datetime import timedelta

from models import Action, BattleState, UserState
from player.workflows import PlayerWorkflow
from temporalio import activity, workflow


@dataclass
class TakeTurnParams:
    username: str
    target: str


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

        current_player = self.state.players[self.state.current_player_index]
        current_player_username = current_player.username

        handle = workflow.get_external_workflow_handle_for(
            PlayerWorkflow.run, current_player_username
        )

        await handle.signal(BattleWorkflow.take_your_turn)

    @workflow.signal
    async def handle_action(self, action: Action) -> None:
        current_player = self.state.players[self.state.current_player_index]

        # out of turn!
        if action.username != current_player.username:
            return

        dice_result = await workflow.execute_activity(
            roll_dice, start_to_close_timeout=timedelta(seconds=5)
        )

        # attack the player that goes after the current player
        next_player = self.state.players[self.state.current_player_index + 1]

        # TODO: calculate damage
        next_player.health -= dice_result

        # update the state
        self.state.players[self.state.current_player_index + 1] = next_player

        # check if the next player is dead
        if next_player.health <= 0:
            # TODO: handle death
            pass

        # update the current player index
        self.state.current_player_index = (self.state.current_player_index + 1) % len(
            self.state.players
        )


@activity.defn
async def roll_dice() -> int:
    import random

    random.seed(workflow.now().timestamp())
    return random.randint(1, 6)
