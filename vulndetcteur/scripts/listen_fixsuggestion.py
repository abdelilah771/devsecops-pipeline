import pika
import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_env():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    if not os.environ.get(key):
                        os.environ[key] = value.strip().strip('"').strip("'")

load_env()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")

def start_spy():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
    
    try:
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        # Declare Exchange (ensure it exists)
        channel.exchange_declare(exchange='logpipeline.exchange', exchange_type='topic', durable=True)

        # Temp buffer queue
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        # Bind to 'vuln.detected'
        channel.queue_bind(exchange='logpipeline.exchange', queue=queue_name, routing_key='vuln.detected')

        logger.info(f"🕵️  Spy listening on 'vuln.detected'. Waiting for messages...")

        def callback(ch, method, properties, body):
            logger.info(f"✅ [Spy] Received message: {body.decode()}")
            data = json.loads(body)
            logger.info(f"   Run ID: {data.get('run_id')}")
            logger.info(f"   Vulnerabilities: {len(data.get('vulnerabilities', []))}")
            # Exit after one message for this test
            ch.stop_consuming()

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()

    except Exception as e:
        logger.error(f"❌ RabbitMQ Connection Failed: {e}")

if __name__ == "__main__":
    start_spy()
