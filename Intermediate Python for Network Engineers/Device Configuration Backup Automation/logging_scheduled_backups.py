import logging

LOG_FORMAT = f'%(asctime)s %(levelname)s %(name)s: %(message)s'
logger = logging.getLogger(__name__)

logging.basicConfig(filename='example.log', level=logging.INFO, filemode='a', format=LOG_FORMAT)

logger.debug("My debug message")
logger.info("My info message")
logger.warning("My warning message")
logger.error("My error message")
logger.critical("My critical message")

logger.setLevel('DEBUG')
logger.debug("Now I get debug messages")