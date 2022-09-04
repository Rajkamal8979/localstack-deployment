import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def lambda_handler(event, context):
    logging.info('Lambda in LocalStack')
    return {
        "message": "Hello User!"
    }