
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.consumer import start_consumer

if __name__ == "__main__":
    print("Starting RabbitMQ Consumer...")
    start_consumer()
