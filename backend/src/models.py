from dataclasses import dataclass
import typing

@dataclass
class UserState:
    username: str
    health: int

@dataclass
class Action:
    username: str
    action_type: str
    description: str

@dataclass
class AIMove:
    action: Action
    new_states: typing.List[UserState]
