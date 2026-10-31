import os
import json

import boto3
from botocore.exceptions import ClientError

sqs = boto3.resource("sqs")


QUEUE_NAME = "test1.fifo"


def send_message():

    queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)
    message_body = json.dumps({
        "boss": "painsmith",
        "limit": 200,
        "metric": "HPS",
    })
    # message_attributes = {
    #     "foo": { "DataType": "String", "StringValue": "test" },
    # }

    try:
        response = queue.send_message(
            MessageBody=message_body,
            # MessageAttributes=message_attributes,
            MessageGroupId="Group-1",
        )
    except ClientError as error:
        print("Send message failed: %s", message_body)
        raise error
    else:
        print("send. ID:", response.get("MessageId"))
        return response


def process_message():

    queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)

    messages = queue.receive_messages(
        AttributeNames=["All"],
        MessageAttributeNames=["*"],
        MaxNumberOfMessages=5,
        # VisibilityTimeout=123,
        WaitTimeSeconds=10,
        # ReceiveRequestAttemptId='string'
    )
    print("-----------")
    for message in messages:
        print("\tID:", message.message_id)
        print("\t", message.message_attributes)
        print("\t", message.body)


if __name__ == "__main__":
    send_message()
    # process_message()
