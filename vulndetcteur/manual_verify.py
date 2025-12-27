import pymongo
import pika
import json
import time
import os
import uuid
from sqlalchemy import create_engine, text

# Configuration
MONGO_URL = os.getenv("MONGO_URL", "mongodb://abdelilahdahou777_db_user:kfsPNTrukGyJxs9a@ac-tthnx18-shard-00-00.ns6lzot.mongodb.net:27017,ac-tthnx18-shard-00-01.ns6lzot.mongodb.net:27017,ac-tthnx18-shard-00-02.ns6lzot.mongodb.net:27017/?authSource=admin&replicaSet=atlas-v9kb86-shard-0&retryWrites=true&w=majority&appName=safeops-logminer&connectTimeoutMS=60000&serverSelectionTimeoutMS=60000&tls=true")
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
POSTGRES_URL = "postgresql://postgres:root@localhost/vulndetec"

RUN_ID = "verify_test_" + str(uuid.uuid4())[:8]
print(f"--- Starting Verification for RUN_ID: {RUN_ID} ---")

def setup_mongo_data():
    print("[1] Setting up MongoDB data...")
    client = pymongo.MongoClient(MONGO_URL)
    db = client["safeops-logminer"]
    col = db["ParsedEvents"]
    
    # Create a dummy event causing a vulnerability
    event = {
        "event_id": str(uuid.uuid4()),
        "run_id": RUN_ID,
        "type": "log",
        "message": "Step uses: actions/checkout@latest which is risky",
        "job_name": "test-job",
        "step_name": "checkout",
        "timestamp": "2025-01-01T12:00:00Z"
    }
    
    col.insert_one(event)
    print(f"    Inserted event into {col.full_name}")
    client.close()

def publish_message():
    print("[2] Publishing RabbitMQ message...")
    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    
    # Ensure exchange exists (consumer should have declared it, but to be safe)
    channel.exchange_declare(exchange='logpipeline.exchange', exchange_type='topic', durable=True)
    
    message = {
        "run_id": RUN_ID,
        "provider": "GITHUB",
        "repo_name": "verify/repo",
        "pipeline_name": "verify-pipeline",
        "environment": "test"
    }
    
    channel.basic_publish(
        exchange='logpipeline.exchange',
        routing_key='logparsed.vuln.detect',
        body=json.dumps(message)
    )
    print(f"    Sent: {message}")
    connection.close()

def check_postgres_and_rabbitmq():
    print("[3] Checking PostgreSQL & RabbitMQ Results...")
    
    # 3a. Check RabbitMQ (First, as it might be faster or buffered)
    print("    [RabbitMQ] Listening for 'vuln.detected' message...")
    try:
        params = pika.URLParameters(RABBITMQ_URL)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        
        # Use the durable queue we declared in main
        queue_name = 'verify_vuln_queue'
        # Ensure it's declared just in case (idempotent)
        channel.queue_declare(queue=queue_name, durable=True)
        
        # We need to wait a bit for the consumer to process and publish
        # Basic consume with timeout
        logger_name = "RabbitMQ-Verifier"
        print(f"    [{logger_name}] waiting for message on {queue_name}...")
        
        method_frame, header_frame, body = next(channel.consume(queue_name, inactivity_timeout=15))
        
        if method_frame:
            data = json.loads(body)
            print(f"    SUCCESS: Received RabbitMQ Message: {data.get('status')} for run_id={data.get('run_id')}")
            print(f"    Vulnerabilities in msg: {len(data.get('vulnerabilities', []))}")
            channel.basic_ack(method_frame.delivery_tag)
        else:
            print("    FAILURE: No RabbitMQ message received (Timeout).")
            
        connection.close()
    except Exception as e:
        print(f"    ERROR checking RabbitMQ: {e}")

    # 3b. Check PostgreSQL
    print("    [PostgreSQL] Verifying DB records...")
    time.sleep(2) 
    
    try:
        engine = create_engine(POSTGRES_URL)
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT count(*) FROM vulnerabilities WHERE run_id = '{RUN_ID}'"))
            count = result.scalar()
            print(f"    Vulnerabilities found in DB: {count}")
            
            if count > 0:
                print("SUCCESS: DB check passed!")
            else:
                print("FAILURE: No vulnerabilities found in PostgreSQL.")
    except Exception as e:
        print(f"    ERROR checking DB: {e}")

if __name__ == "__main__":
    try:
        setup_mongo_data()
        # Start a listener thread or just rely on the queue holding it? 
        # Since we bind AFTER publishing in the previous logic, we might miss it if exchange type is Topic/Direct without a durable queue.
        # But here we used a temporary queue bound AFTER processing started?
        # Ideally, we should bind BEFORE publishing.
        # Let's simple-hack: Split the script or assume the queue "vuln.detected" might already exist if FixSuggester created it?
        # No, better: Create the binding BEFORE publishing.
        
        # Redoing flow logic in main:
         
        # 1. Setup Mongo
        # 2. Bind verify queue (so we don't miss the message)
        params = pika.URLParameters(RABBITMQ_URL)
        conn = pika.BlockingConnection(params)
        ch = conn.channel()
        ch.exchange_declare(exchange='logpipeline.exchange', exchange_type='topic', durable=True)
        q_res = ch.queue_declare(queue='', exclusive=True)
        verify_q = q_res.method.queue
        ch.queue_bind(exchange='logpipeline.exchange', queue=verify_q, routing_key='vuln.detected')
        conn.close()
        
        publish_message()
        
        # 3. Consume from the queue created above
        # Need to reconnect to consume from that specific exclusive queue? 
        # Exclusive queues are deleted when connection closes. 
        # FIX: We need to keep connection open or use a named durable queue for verification.
        # Let's use a named durable queue for test "verify_vuln_queue"
        
        params = pika.URLParameters(RABBITMQ_URL)
        conn = pika.BlockingConnection(params)
        ch = conn.channel()
        ch.exchange_declare(exchange='logpipeline.exchange', exchange_type='topic', durable=True)
        ch.queue_declare(queue='verify_vuln_queue', durable=True)
        ch.queue_bind(exchange='logpipeline.exchange', queue='verify_vuln_queue', routing_key='vuln.detected')
        conn.close()
        
        check_postgres_and_rabbitmq() # This function needs to read from 'verify_vuln_queue' now.
    except Exception as e:
        print(f"ERROR: {e}")
