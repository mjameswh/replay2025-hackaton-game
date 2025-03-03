from datetime import timedelta

from temporalio import workflow

# Import activity for writing to player's socket
with workflow.unsafe.imports_passed_through():
    from activities import write_to_socket


@workflow.defn
class PlayerWorkflow:
    @workflow.signal
    async def take_turn(self, TakeTurnParams) -> None:
        """
        Received from the Battle workflow.
        For human players, write a message to the player's socket and await their response on the "player_response" signal.
        For NPCs, roll a d6 dice to determine the outcome.
        """
        pass

    @workflow.signal
    async def player_response(message: str) -> None:
        """
        Handles the response from the player.

        For now, they can just attack the target
        """
        await write_to_socket(
            username=username, message=message, timeout=timedelta(seconds=5)
        )
