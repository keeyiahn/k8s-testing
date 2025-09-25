import psycopg2
from confluent_kafka import Consumer
import json

group = "postgres-consumer"
conf = {
    #'bootstrap.servers': 'localhost:9094',
    "bootstrap.servers": "kafka-controller-0.kafka-controller-headless.default.svc.cluster.local:9092, kafka-controller-1.kafka-controller-headless.default.svc.cluster.local:9092, kafka-controller-2.kafka-controller-headless.default.svc.cluster.local:9092",
    'group.id': group,
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['test-topic'])

def add_to_db(name, age):
    conn = psycopg2.connect(
        host="postgres-service",
        database="flaskdb",
        user="flaskuser",
        password="flaskpass",
        port=5432
    )

    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s);", (name, age))
    conn.commit()
    cursor.close()
    conn.close()

i = 0
try:
    while True:
        msg = consumer.poll(1.0)  # timeout in seconds
        if msg is None:
            print(str(i) + " No new messages")
            i+=1
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        data = json.loads(msg.value().decode('utf-8'))
        name = data.get("name")
        age = data.get("age")
        print(name, age)
        add_to_db(name, age)
finally:
    consumer.close()

