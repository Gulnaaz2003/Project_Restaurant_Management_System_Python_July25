import datetime
import os
import traceback

def error_logs(data, error_type="Exception", extra_info=None):
    
    os.makedirs("logs", exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    
    log_entry = [
        "\n" + "=" * 80,
        f"TIMESTAMP : {timestamp}",
        f"{traceback.format_exc()}",
        "=" * 80 + "\n"
    ]

    
    with open("logs/log.txt", "a") as file:
        file.write("\n".join(log_entry))