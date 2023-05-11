import logging
from app_tasks import CreateFolderTask

logging.basicConfig(level=logging.DEBUG)

logging.debug("A debug message")
logging.info("An info message")
logging.warning("A warning message")
logging.error("An error message")
logging.critical("A critical message")
logging.info(f"{__file__:s}")
logging.info(f"{__name__:s}")

task = CreateFolderTask('test', None)

task.execute()
