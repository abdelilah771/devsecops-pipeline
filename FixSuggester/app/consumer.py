import pika
import json
import asyncio
from app.core.config import settings
from app.services.fix_generator import FixGenerator

# Global generator instance
fix_generator = FixGenerator()

def start_fix_suggester():
    try:
        url = settings.RABBITMQ_URL
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        # 1. Declare Exchange
        channel.exchange_declare(exchange='logpipeline.exchange', exchange_type='topic', durable=True)

        # 2. Declare Queue
        queue_name = 'fixsuggester.queue'
        channel.queue_declare(queue=queue_name, durable=True)

        # 3. Bind Queue
        channel.queue_bind(exchange='logpipeline.exchange', queue=queue_name, routing_key='vuln.detected')

        print(f" [*] FixSuggester waiting for 'vuln.detected' events on {queue_name}...")

        def on_message(ch, method, properties, body):
            try:
                payload = json.loads(body)
                run_id = payload.get("run_id")
                vulns = payload.get("vulnerabilities", [])
                
                print(f" [!] Received {len(vulns)} vulnerabilities for Run: {run_id}")
                
                # Since pika is blocking and FixGenerator is async, we need a way to run async code.
                # For simplicity in this worker, we can use asyncio.run or create a loop.
                # However, re-creating the loop for every message is inefficient. 
                # A better approach for production is using aio-pika, but user provided pika example.
                # We will use asyncio.run() for this iteration as it's a simple consumer.
                
                for v in vulns:
                    # Enrich vulnerability data if needed, or pass as is
                    print(f"     Processing: {v.get('owasp_category', 'Unknown')}")
                    asyncio.run(fix_generator.generate_from_event(v))
                
                ch.basic_ack(delivery_tag=method.delivery_tag)
                
            except Exception as e:
                print(f" [x] Error processing message: {e}")
                # Don't requeue bad messages to avoid loops
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queue_name, on_message_callback=on_message)
        channel.start_consuming()

    except Exception as e:
        print(f" [x] Connection failed: {e}")

if __name__ == "__main__":
    start_fix_suggester()
