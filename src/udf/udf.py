from pynumaflow.mapper import Messages, Message, Datum, MapServer
import json

def my_handler(keys: list[str], datum: Datum) -> Messages:
    val = datum.value
    output_keys = keys
    output_tags = []
    _ = datum.event_time
    _ = datum.watermark
    messages = Messages()
    data = json.loads(val)
    name = data["name"]
    age = data["age"]
    try:
        if int(age):
            output_keys = ["users"]
            output_tags = ["users-tag"]
    except Exception as e:
        output_keys = ["error"]
        output_tags = ["error-tag"]
    
    print(f"val: {data}, key:{output_keys}")
    messages.append(Message(val, keys=output_keys, tags=output_tags))
    return messages

if __name__ == "__main__":
    grpc_server = MapServer(my_handler)
    grpc_server.start()