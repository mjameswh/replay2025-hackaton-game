from temporalio import workflow

# Import activity, passing it through the sandbox without reloading the module
with workflow.unsafe.imports_passed_through():
    from npc.activities import ai_make_move


@workflow.defn
class NpcWorkflow:
    def __init__(self) -> None:
        self.should_proceed = False
        self.states = []
        self.actions = []

    @workflow.run
    async def run(self, name: str) -> str:
        while (True):
            await workflow.wait_condition(lambda: self.should_proceed)
            resp = await ai_make_move(self.states, self.actions, name)

            # TODO: send signal to battle

    @workflow.signal
    def proceed(self, states) -> None:
        self.should_proceed = True
        self.states = states

