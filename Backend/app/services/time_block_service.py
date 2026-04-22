from datetime import datetime
from app.utils.time_helpers import get_time_block


def get_current_time_block() -> str:
    """Returns the time block for right now."""
    return get_time_block(datetime.now())


def get_time_block_for(dt: datetime) -> str:
    """Returns the time block for any given datetime."""
    return get_time_block(dt)