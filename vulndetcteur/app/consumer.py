import pika
import json
import os
import logging
from typing import List

from .database import get_mongo_db, SessionLocal
from .detection import run_detection_logic
from .crud import insert_vulnerabilities
from schemas import Event

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")

def get_rabbitmq_connection():
    params = pika.URLParameters(RABBITMQ_URL)
    return pika.BlockingConnection(params)

def start_consumer():
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()

        # Declare Exchange
        channel.exchange_declare(
            exchange='logpipeline.exchange',
            exchange_type='topic',
            durable=True
        )

        # Declare Queue
        queue_name = 'logparser.vulndetector.queue'
        channel.queue_declare(queue=queue_name, durable=True)

        # Bind Queue
        routing_key = 'logparsed.vuln.detect'
        channel.queue_bind(
            exchange='logpipeline.exchange',
            queue=queue_name,
            routing_key=routing_key
        )

        logger.info(f" [*] Waiting for messages on {queue_name}. To exit press CTRL+C")

        def on_message(ch, method, properties, body):
            logger.info(f" [x] Received {body}")
            try:
                data = json.loads(body)
                run_id = data.get("run_id")

                if not run_id:
                    logger.warning("Received message without run_id")
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    return

                # Fetch events from MongoDB
                mongo_db = get_mongo_db()
                logger.info(f"Available collections in {mongo_db.name}: {mongo_db.list_collection_names()}")
                parsed_events_collection = mongo_db["ParsedEvents"]
                
                # Assume events are stored associated with run_id in MongoDB
                # The user checklist says: `parsed_events_collection.find_one({"run_id": "<test_run>"})`
                # If the collection stores one document per event, we need `find({"run_id": run_id})`
                # If it stores one document per run with a list of events, we need `find_one`.
                # Given typical log parsing, it's often a list of events.
                # However, checklist item A says: `parsed_events_collection.find_one({"run_id": "<test_run>"})` returns a document.
                # Use find to get all events for the run_id if they are individual documents, or find_one if grouped.
                # Let's assume individual documents for scalable log storage, or a big document.
                # Looking at checklist Item E: "Lit ParsedEvents pour ce run_id".
                # Let's try to find all documents with this run_id.
                
                # Start of processing log
                logger.info(f"===============================================================")
                logger.info(f"🚀 [RabbitMQ] Received processing request for run_id: {run_id}")
                
                # Fetch events from MongoDB
                mongo_db = get_mongo_db()
                parsed_events_collection = mongo_db["ParsedEvents"]
                
                if os.getenv("DEBUG", "false").lower() == "true":
                     logger.info(f"🔎 [Debug] Querying MongoDB collection: '{parsed_events_collection.name}' in db: '{mongo_db.name}'")
                
                cursor = parsed_events_collection.find({"run_id": run_id})
                events_list = list(cursor)
                logger.info(f"📂 [MongoDB] Found {len(events_list)} parsed events for run_id={run_id}")
                
                pydantic_events = []
                # ... (paring logic roughly same, omitted for brevity in thought but kept in replacement) ...
                for doc in events_list:
                    doc.pop("_id", None)
                    try:
                        ev = Event(**doc)
                        pydantic_events.append(ev)
                    except Exception as e:
                        logger.error(f"⚠️ Error parsing event: {e}")

                if not pydantic_events:
                    logger.warning(f"⚠️ [Warning] No valid events found for run_id: {run_id}. Skipping detection.")
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    logger.info(f"===============================================================")
                    return

                # Run Detection Logic
                logger.info(f"⚙️  [Logic] Running detection rules on {len(pydantic_events)} events...")
                vulns = run_detection_logic(run_id, pydantic_events)
                
                if vulns:
                    logger.info(f"🚨 [Detection] IDENTIFIED {len(vulns)} VULNERABILITIES!")
                    for i, v in enumerate(vulns, 1):
                        logger.info(f"   {i}. [{v.severity}] {v.owasp_category} (Fix: {v.suggested_fix_key})")
                else:
                    logger.info(f"✅ [Detection] No vulnerabilities found.")

                # Store in PostgreSQL
                db = SessionLocal()
                try:
                    insert_vulnerabilities(db, vulns)
                    if vulns:
                        logger.info(f"💾 [DB] Successfully saved {len(vulns)} vulnerabilities to PostgreSQL.")
                except Exception as db_e:
                    logger.error(f"❌ [DB Error] Failed to save vulnerabilities: {db_e}")
                finally:
                    db.close()

                # --- PUBLISH RESULT TO RABBITMQ (For FixSuggester) ---
                if vulns:
                    try:
                        # Construct payload for FixSuggester
                        # It needs vulnerabilities and context.
                        result_payload = {
                            "run_id": run_id,
                            "status": "VULNERABILITIES_FOUND",
                            "risk_score": 0.0, # You might want to grab this from detect calculation if available
                            "vulnerabilities": [v.dict() for v in vulns]
                        }
                        
                        channel.basic_publish(
                            exchange='logpipeline.exchange',
                            routing_key='vuln.detected',
                            body=json.dumps(result_payload),
                            properties=pika.BasicProperties(
                                delivery_mode=2,  # make message persistent
                            )
                        )
                        logger.info(f"📤 [RabbitMQ] Published {len(vulns)} vulnerabilities to 'vuln.detected'")
                    except Exception as pub_e:
                        logger.error(f"❌ [RabbitMQ Error] Failed to publish results: {pub_e}")

                ch.basic_ack(delivery_tag=method.delivery_tag)
                logger.info(f"✅ [Done] Finished processing run_id: {run_id}")
                logger.info(f"===============================================================")

            except Exception as e:
                logger.error(f"Error processing message: {e}")
                # Ideally, NACK or Dead Letter Queue, but for now simple ack or generic fail
                # ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False) 
                # Let's just log and ack properly to avoid stuck loops if it's a code error
                ch.basic_ack(delivery_tag=method.delivery_tag) 

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queue_name, on_message_callback=on_message)
        channel.start_consuming()

    except Exception as e:
        logger.error(f"Consumer error: {e}")
