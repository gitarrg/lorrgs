from lorrgs_sqs import helpers


def test_queue_arn_to_url():

    arn = "arn:aws:sqs:eu-west-1:12345678:my_queue.fifo"
    url = helpers.queue_arn_to_url(arn)
    assert url == "https://sqs.eu-west-1.amazonaws.com/12345678/my_queue.fifo"


if __name__ == "__main__":
    test_queue_arn_to_url()
