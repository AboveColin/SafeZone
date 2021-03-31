import logging
from colorlog import ColoredFormatter

def setup_logger():
    """Return a logger with a default ColoredFormatter."""
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)-2s%(reset)s [%(cyan)s%(asctime)s%(white)s] %(message)s",
        datefmt='%d-%m %H:%M:%S',
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red'
        }
    )

    logger = logging.getLogger('example')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger

logger = setup_logger()

f_log = logging.getLogger('werkzeug')
f_log.setLevel(logging.ERROR)