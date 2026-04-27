import sys
from loguru import logger

def setup_logging():
    logger.remove()  # hapus default handler
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function} | {message}",
        level="INFO"
    )