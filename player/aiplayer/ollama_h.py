import ollama

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

def run_command_ai(text: str):
    # print(text)
    resp = ollama.chat(model='llama3.2:latest', messages=[{'role': 'user', 'content': text}])
    # print(resp['message']['content'])
    return resp['message']['content']

def process_move(
    history: typing.List[Action],
    states: typing.List[UserState],
    name: str) -> AIMove:

    response_format = 'First line - event description, '
    for i in range(len(states)):
        response_format += f'line {i + 2}: new health for {states[i].username} (only number), '
    
    text = (f'You are monster in a D&D game. Your name is {name}. It is your move now. Here is a list of last moves. '
    f'U need to response for the last one. Actual health states: {str(states)}. Answer with an action (in the third person) and new states'
    f'Response format: {response_format}')

    data = []

    while len(data) != 2 + len(states):
        new_state = run_command_ai(text)
        data = new_state.split('\n')

    move = AIMove(action=data[0], new_states=[])

    for i in range(len(states)):
        move.new_states.append(UserState(username=states[i].username, health=int(data[i+2])))
    
    return move

action1 = Action(action_type='attack', description='Take a big stick', username='Player1')

state1 = UserState(health=100, username='Player1')

state2 = UserState(health=100, username='Wolf1')

print(process_move([action1], [state1, state2], 'Wolf1'))