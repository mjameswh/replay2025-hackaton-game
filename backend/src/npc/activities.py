from temporalio import activity
from llm import ollama_h

import typing
import models

@activity.defn
async def say_hello(name: str) -> str:
    return f"Hello, {name}!"

@activity.defn
async def ai_make_move(
    history: typing.List[models.Action],
    states: typing.List[models.UserState],
    username: str) -> models.AIMove:
    
    return ollama_h.process_move(history, states, username)