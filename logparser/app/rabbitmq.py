
import json
import pika
import logging
from app.config import settings

logger = logging.getLogger("RabbitMQ")

def check_connection() -> bool:
    """
    Checks if RabbitMQ is reachable.
    """
    try:
        params = pika.URLParameters(settings.rabbitmq_url)
        # Set short timeout for health check
        params.socket_timeout = 2 
        params.connection_attempts = 1
        params.retry_delay = 0
        connection = pika.BlockingConnection(params)
        if connection.is_open:
            connection.close()
            return True
        return False
    except Exception as e:
        logger.error(f"RabbitMQ health check failed: {e}")
        return False

def publish_parsing_result(payload: dict):
    """
    Publishes the parsed event result to RabbitMQ.
    """
    try:
        # Establish blocking connection
        params = pika.URLParameters(settings.rabbitmq_url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        # Declare the exchange (idempotent)
        exchange_name = "logpipeline.exchange"
        channel.exchange_declare(
            exchange=exchange_name,
            exchange_type="topic",
            durable=True
        )

        # Declare the queue (idempotent)
        queue_name = "logparser.vulndetector.queue"
        channel.queue_declare(
            queue=queue_name,
            durable=True
        )
        
        # Binding
        routing_key = "logparsed.vuln.detect"
        channel.queue_bind(
            exchange=exchange_name,
            queue=queue_name,
            routing_key=routing_key
        )

        # Publish message
        channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=json.dumps(payload),
            properties=pika.BasicProperties(
                content_type="application/json",
                delivery_mode=2  # make message persistent
            )
        )
        
        logger.info(f"Sent payload to {exchange_name} with key {routing_key}")
        connection.close()
        return True
    except Exception as e:
        logger.error(f"Failed to publish to RabbitMQ: {e}")
        return False
