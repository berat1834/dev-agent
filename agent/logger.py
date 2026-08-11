import logging
import sys
from pathlib import Path

LOG_DIR = Path.home() / ".agent"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "agent.log"

def setup_logger(name: str = "dev_agent") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Console Handler
        c_handler = logging.StreamHandler(sys.stdout)
        c_format = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s', datefmt='%H:%M:%S')
        c_handler.setFormatter(c_format)
        logger.addHandler(c_handler)

        # File Handler
        f_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(f_format)
        logger.addHandler(f_handler)

    return logger

logger = setup_logger()