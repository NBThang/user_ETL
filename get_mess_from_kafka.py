from confluent_kafka import Consumer

conf = {
    'bootstrap.servers': '192.168.33.109:9092',  # phải đúng với advertised.listeners
    'group.id': 'my-consumer-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['pg1.public.users'])

print("Đang chờ message từ Kafka...")

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            print("Lỗi:", msg.error())
        else:
            print(f"Message: {msg.value().decode('utf-8')}")
except KeyboardInterrupt:
    print("Dừng.")
finally:
    consumer.close()
