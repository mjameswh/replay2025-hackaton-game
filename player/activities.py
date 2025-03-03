from temporalio import activity
import typing

import models

@activity.defn
async def say_hello(name: str) -> str:
    return f"Hello, {name}!"

@activity.defn
async def ai_make_move(
    history: typing.List[models.Action],
    states: typing.List[models.UserState]) -> models.AIMove:
    return (None, None)
