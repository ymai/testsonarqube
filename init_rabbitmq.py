import pika


HOST_URL = 'amqp://guest:guest@localhost:5673'
EXCHANGES_AND_QUEUES = {'task_exchange': [{'queue_name': 'nongpu_tasks', 'routing_key': 'nongpu'},
                                          {'queue_name': 'gpu_tasks', 'routing_key': 'gpu'}],
                        'result_exchange': [{'queue_name': 'task_results_queue', 'routing_key': 'result'}]}


if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.URLParameters(HOST_URL))
    channel = connection.channel()

    for exchange, queue_config in EXCHANGES_AND_QUEUES.items():
        channel.exchange_declare(exchange, exchange_type='topic')

        for queue_info in queue_config:
            queue_name = queue_info['queue_name']
            routing_key = queue_info['routing_key']

            channel.queue_declare(queue=queue_name)
            channel.queue_bind(queue_name, exchange, routing_key=routing_key)
