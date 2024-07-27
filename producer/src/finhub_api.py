import websocket
import json
from producer import Producer


kafka_producer = Producer(schema_reg_url="http://schema-registry:8081", topic_name="live-stock")
    

def on_message(ws, message):
    json_data = json.loads(message)
    print(json.dumps(json_data, indent=4))
    kafka_producer.produce(json_data)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"AAPL"}')
    ws.send('{"type":"subscribe","symbol":"AMZN"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
    ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')

if __name__ == "__main__":
    #kafka_producer = producer.Producer(schema_reg_url="https://localhost:8081", topic_name="live-stock")
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=cq6cms9r01qlbj500a0gcq6cms9r01qlbj500a10",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

