import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def lamda_handler(event, context):
    logging.info('Lambda in LocalStack')
    return {
        "message": "Hello User!"
    }