import logging
from logging.handlers import TimedRotatingFileHandler

LOG_FORMAT = f'%(asctime)s %(levelname)s %(name)s: %(message)s'
logger = logging.getLogger(__name__)
handler = TimedRotatingFileHandler('example.log', when='D', interval=1, backupCount=2)

formatter = logging.Formatter(LOG_FORMAT)
handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO, handlers=[handler])

logger.debug("My debug message")
logger.info("My info message")
logger.warning("My warning message")
logger.error("My error message")
logger.critical("My critical message")

logger.setLevel('DEBUG')
logger.debug("Now I get debug messages")