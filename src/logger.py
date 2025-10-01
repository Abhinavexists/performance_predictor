import os
import sys
import logging
from datetime import datetime
from pathlib import Path

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}"
logs_path = Path.cwd() / 'logs' / LOG_FILE
LOG_FILE_PATH = Path.joinpath(logs_path, LOG_FILE)
os.makedirs(logs_path, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),
        logging.StreamHandler(sys.stdout)
    ]
)
