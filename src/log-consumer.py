from confluent_kafka import Consumer


group = "log-consumer"
conf = {
    #'bootstrap.servers': 'localhost:9094',
    "bootstrap.servers": "kafka-controller-0.kafka-controller-headless.default.svc.cluster.local:9092, kafka-controller-1.kafka-controller-headless.default.svc.cluster.local:9092, kafka-controller-2.kafka-controller-headless.default.svc.cluster.local:9092",
    'group.id': group,
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['test-topic'])

print(f" Listening for messages... group: {group}", flush=True)
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
        print(f"Received message: {msg.value().decode('utf-8')} (key={msg.key()})")
finally:
    consumer.close()
 