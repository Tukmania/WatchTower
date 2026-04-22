from datetime import datetime


def get_time_block(dt: datetime) -> str:
    minutes = dt.hour * 60 + dt.minute
    block_start_minutes = (minutes // 30) * 30
    block_end_minutes = block_start_minutes + 30

    start_h = block_start_minutes // 60
    start_m = block_start_minutes % 60
    end_h   = block_end_minutes // 60
    end_m   = block_end_minutes % 60

    # Roll 24:00 over to 00:00
    if end_h >= 24:
        end_h = 0

    start = f"{start_h:02d}:{start_m:02d}"
    end   = f"{end_h:02d}:{end_m:02d}"

    return f"{start} – {end}"