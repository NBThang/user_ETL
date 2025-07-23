from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'pg1.public.users',  # thay bằng tên topic thực tế
    bootstrap_servers='192.168.33.109:9092',  # vì bạn dùng host.docker.internal:9092
    auto_offset_reset='earliest',  # đọc từ đầu
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: x.decode('utf-8')
)

print("Đang đợi message...")
for message in consumer:
    print(f"Message nhận được: {message.value}")
