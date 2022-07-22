import logging
import os
import datetime



logging.basicConfig(filename="logs/log.txt",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logging.info("Running Logger")

logger = logging.getLogger('urbanGUI')