import logging
import json
import uuid
import time
import threading
from unittest.mock import MagicMock, patch
import pika

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add project root to sys.path
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the consumer function (we will patch its internal get_mongo_db)
from app.consumer import start_consumer

# Mock Event Data that triggers a vulnerability
MOCK_EVENT = {
    "run_id": "test_mock_run",
    "event_id": str(uuid.uuid4()),
    "job_name": "test-job",
    "step_name": "test-step",
    "message": "AWS_ACCESS_KEY_ID=AKIA_MOCK_SECRET", # Triggers secret leak rule
    "timestamp": "2023-10-27T10:00:00Z"
}

def mock_get_mongo_db():
    logger.info("🔧 [Mock] get_mongo_db called. Returning mock DB.")
    mock_db = MagicMock()
    mock_collection = MagicMock()
    
    # Mock find() to return our list of events
    mock_cursor = [MOCK_EVENT]
    mock_collection.find.return_value = mock_cursor
    
    mock_db.__getitem__.return_value = mock_collection # db["ParsedEvents"]
    mock_db.list_collection_names.return_value = ["ParsedEvents"]
    mock_db.name = "mock_db"
    return mock_db

def run_consumer_mocked():
    # Patch get_mongo_db in app.consumer
    with patch('app.consumer.get_mongo_db', side_effect=mock_get_mongo_db):
        # We also need to patch database.insert_vulnerabilities so we don't need real Postgres
        # Or we can let it fail gracefully (consumer catches generic exceptions?).
        # Consumer code:
        # try: insert_vulnerabilities... except: logger.error...
        # It catches exception, so even if Postgres fails, it SHOULD proceed to Publish?
        # Lines 119-126: db save. Lines 129+: publish.
        # Yes, publish is AFTER db save. If db save fails, does it stop?
        # Logic: `    except Exception as db_e: logger.error... finally: db.close()`
        # It proceeds to `if vulns: ... publish`.
        # So we don't strictly need to mock Postgres, but let's mock it to be clean.
        
        with patch('app.consumer.SessionLocal') as mock_session:
            # Also patch pika connection to just spy on publish? 
            # No, we want to actually publish to RabbitMQ to verify the queue receives it.
            # So we use REAL RabbitMQ connection.
            logger.info("🚀 Starting Mocked Consumer...")
            start_consumer()

def trigger_and_listen():
    # 1. Start Consumer in a thread
    consumer_thread = threading.Thread(target=run_consumer_mocked)
    consumer_thread.daemon = True
    consumer_thread.start()
    
    # Give it a second to connect
    time.sleep(2)
    
    # 2. Publish Trigger Message (LogParser -> VulnDetector)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='logpipeline.exchange', exchange_type='topic', durable=True)
    
    trigger_msg = {"run_id": "test_mock_run", "status": "LOGS_PARSED"}
    channel.basic_publish(
        exchange='logpipeline.exchange',
        routing_key='logparsed.vuln.detect',
        body=json.dumps(trigger_msg)
    )
    logger.info("📥 [Trigger] Sent message to logparsed.vuln.detect")
    
    # 3. Listen for Output (VulnDetector -> FixSuggestion)
    # Queue for spy
    result = channel.queue_declare(queue='', exclusive=True)
    callback_queue = result.method.queue
    channel.queue_bind(exchange='logpipeline.exchange', queue=callback_queue, routing_key='vuln.detected')
    
    logger.info("👀 [Spy] Listening for 'vuln.detected'...")
    
    def on_response(ch, method, props, body):
        logger.info(f"✅ [Success] Received FixSuggestion message: {body.decode()}")
        ch.stop_consuming()
        logger.info("🎉 Verification Complete: Message successfully flowed from LogParser -> VulnDetector -> FixSuggestion!")
        # We can kill the process now
        import os, signal
        os.kill(os.getpid(), signal.SIGTERM)

    channel.basic_consume(queue=callback_queue, on_message_callback=on_response, auto_ack=True)
    
    # Wait for 10 seconds max
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f"Error in spy: {e}")

if __name__ == "__main__":
    trigger_and_listen()
