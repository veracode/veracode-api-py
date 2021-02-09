# Purpose:  Log utilities

import logging
import time
from datetime import datetime

class VeracodeLog():
    def setup_logging(self,debug=False):
        now = datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
        format_string = "%(asctime)s %(levelname)s %(message)s"
        datetime_format = '%Y-%m-%d %H:%M:%S %Z'

        logging.captureWarnings(True)
        logging.Formatter.converter = time.gmtime

        if debug:
            logging.basicConfig(format=format_string, datefmt=datetime_format, filename="{}-debug.log".format(now), level=logging.DEBUG)
        else:
            logging.basicConfig(format=format_string, datefmt=datetime_format, filename="{}.log".format(now), level=logging.INFO)
            requests_logger = logging.getLogger("requests")
            requests_logger.setLevel(logging.WARNING)
