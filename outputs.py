from app import get_logger, get_config
import boto3

from utils import chunk_it, jsonify

config = get_config()
my_logger = get_logger()


def to_log_file(data):
    if isinstance(data, list):
        for i in data:
            my_logger.info(i)
    else:
        my_logger.info(data)


def to_firehose(data):
    conn = boto3.client('firehose', region_name="us-east-1", aws_access_key_id=config.AWS_ACCESS_KEY, aws_secret_access_key=config.AWS_SECRET_KEY)
    if isinstance(data, list):
        for group in chunk_it(data, 500):
            conn.put_record_batch(DeliveryStreamName=config.AWS_FIREHOSE_DELIVERY_STREAM_NAME,
                                  Records=[{"Data": jsonify(i)} for i in group])
    else:
        conn.put_record(DeliveryStreamName=config.AWS_FIREHOSE_DELIVERY_STREAM_NAME,
                        Record=jsonify(data))
