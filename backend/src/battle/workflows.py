from temporalio import workflow


@workflow.defn
class BattleWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        pass
