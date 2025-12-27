import pika
from app.config.settings import settings

def get_rabbitmq_connection(heartbeat=600, socket_timeout=2):
    """Crée connexion RabbitMQ"""
    credentials = pika.PlainCredentials(
        settings.RABBITMQ_USER,
        settings.RABBITMQ_PASS
    )
    parameters = pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        credentials=credentials,
        heartbeat=heartbeat,
        blocked_connection_timeout=300,
        # Health check optimizations
        socket_timeout=socket_timeout,
        connection_attempts=1,
        retry_delay=0
    )
    return pika.BlockingConnection(parameters)

def get_consumer_connection():
    """Crée connexion RabbitMQ stable pour le consumer"""
    credentials = pika.PlainCredentials(
        settings.RABBITMQ_USER,
        settings.RABBITMQ_PASS
    )
    parameters = pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        credentials=credentials,
        heartbeat=0,  # Disable heartbeat to prevent timeouts during processing
        blocked_connection_timeout=300
    )
    return pika.BlockingConnection(parameters)

def get_channel():
    """Crée channel RabbitMQ"""
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    
    # Use standard connection for health checks / publishing
    # For consumer, we might want to use get_consumer_connection specifically?
    # But for now, let's just make the default get_rabbitmq_connection robust enough
    # by modifying it to be less aggressive if called with arguments, 
    # OR better yet, let's update get_rabbitmq_connection to take an optional 'for_consumer' flag.
    

    
    # Declare queues (idempotent)
    channel.queue_declare(
        queue=settings.QUEUE_RAW_LOGS,
        durable=True
    )
    
    # Declare Exchange
    channel.exchange_declare(
        exchange=settings.RABBITMQ_EXCHANGE,
        exchange_type="topic",
        durable=True
    )

    # Declare Destination Queue
    channel.queue_declare(
        queue=settings.QUEUE_PARSED_EVENTS,
        durable=True
    )
    
    # Bind Queue to Exchange
    channel.queue_bind(
        exchange=settings.RABBITMQ_EXCHANGE,
        queue=settings.QUEUE_PARSED_EVENTS,
        routing_key=settings.RABBITMQ_ROUTING_KEY
    )
    
    return connection, channel
