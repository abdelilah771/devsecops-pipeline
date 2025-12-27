import json
import pika
from app.config.settings import settings
from app.messaging.rabbitmq import get_channel, get_rabbitmq_connection
from app.parser.yaml_parser import parse_workflow
from app.parser.feature_extractor import extract_security_features
from app.messaging.publisher import publish_parsed_event

def callback(ch, method, properties, body):
    """Callback appelé pour chaque message"""
    try:
        # Décoder message
        message = json.loads(body)
        print(f"📥 Received message: {message.get('repository', 'unknown')}")
        
        # Parser workflow
        workflow_yaml = message.get('workflow', {})
        parsed = parse_workflow(workflow_yaml)
        features = extract_security_features(parsed) # Extraction ajoutée
        
        # Publier event parsé
        publish_parsed_event({
            'repository': message.get('repository'),
            'parsed_workflow': parsed,
            'features': features,
            'original_id': message.get('_id')
        })
        
        # Acknowledge message
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("✅ Message processed and published")
        
    except Exception as e:
        print(f"❌ Error processing message: {e}")
        # Reject message (DLQ)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def start_consumer():
    """Démarre le consumer (bloquant)"""
    try:
        print("🔌 Connecting to RabbitMQ Consumer...")
        # Use 0 heartbeat and None/Long timeout for stable consumer connection
        connection = get_rabbitmq_connection(heartbeat=0, socket_timeout=None)
        channel = connection.channel()
        
        # Declare topology here again just in case
        pass # Channel already obtained above via new conn
        
        # Declare queues (idempotent)
        channel.queue_declare(queue=settings.QUEUE_RAW_LOGS, durable=True)
        channel.basic_qos(prefetch_count=1)  # 1 message à la fois
        channel.basic_consume(
            queue=settings.QUEUE_RAW_LOGS,
            on_message_callback=callback,
            auto_ack=False  # Manual ACK
        )
        
        print(f"👂 Listening on queue: {settings.QUEUE_RAW_LOGS}")
        channel.start_consuming()
        
    except KeyboardInterrupt:
        print("🛑 Consumer stopped")
        connection.close()
    except Exception as e:
        print(f"❌ Consumer error: {e}")
