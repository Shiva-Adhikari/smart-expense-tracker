import logging
from src.core.config import settings

def create_logger():
    log = logging.getLogger(__name__)

    DEBUG_LEVEL = settings.DEBUG_LEVEL.get_secret_value()
    log.setLevel(logging.DEBUG)

    # Create handler and formatter
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s | %(asctime)s | %(filename)s | def: %(funcName)s | Lineno: %(lineno)s >> "%(message)s"')
    handler.setFormatter(formatter)
    log.addHandler(handler)

    return log


logger = create_logger()
