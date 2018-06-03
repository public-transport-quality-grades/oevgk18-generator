def get_filename_from_due_date_config(due_date_config: dict) -> str:
    return f"oevgk18_{due_date_config['due-date'].strftime('%Y-%m-%d')}_" \
           f"{due_date_config['type-of-interval']}.geojson"
