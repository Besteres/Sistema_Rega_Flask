import time
import datetime

import logger

log = logger.Logger()

def print_data(data):
    print(data)

log.on_data_updated(print_data)

while True:
    print(datetime.datetime.today())
    time.sleep(1.0)