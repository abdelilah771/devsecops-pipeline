import json
import pika
from app.config.settings import settings
from app.messaging.rabbitmq import get_channel

def publish_parsed_event(event: dict):
    """Publie event parsé dans queue"""
    try:
        connection, channel = get_channel()
        
        # Publier message
        channel.basic_publish(
            exchange=settings.RABBITMQ_EXCHANGE,
            routing_key=settings.RABBITMQ_ROUTING_KEY,
            body=json.dumps(event),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Persistent
                content_type='application/json'
            )
        )
        
        print(f"📤 Published to {settings.QUEUE_PARSED_EVENTS}")
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Publish error: {e}")
        return False
