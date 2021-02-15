
import logging
import os
from molasses import MolassesClient
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
client = MolassesClient(os.environ.get('MOLASSES_API_KEY'))
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
count = 0
current_value = False

while True:
    # if count > 40:
    #     break
    new_value = client.is_active('Test')
    if new_value != current_value:
        logging.info("NEW VALUE %s", new_value)
        current_value = new_value
