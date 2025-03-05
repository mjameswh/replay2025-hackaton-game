from temporalio import activity

@activity.defn
async def story_event(event: str) -> str:
    return f"Story Event: {event}!"