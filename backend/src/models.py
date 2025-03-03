import typing
from dataclasses import dataclass


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


@dataclass
class BattleState:
    players: list[UserState]  # ordered in turn order
    current_player_index: int
