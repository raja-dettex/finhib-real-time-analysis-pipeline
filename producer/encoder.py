import io
import fastavro
import os

def get_schema():
    import os
    import json
    
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'schema.avsc')
    print(path)
    with open(path, 'r') as f:
        schema = json.load(f)
        return schema
    

def encode(schema=None, data=None):
    buffer = io.BytesIO()
    fastavro.schemaless_writer(buffer, schema, data)
    value = buffer.getvalue()
    return value


def decode(schema=None, value=None):
    buffer = io.BytesIO(value)
    data = fastavro.schemaless_reader(buffer, schema)
    return data
    

if __name__ == '__main__':
    schema = get_schema()
    example_data = example_data = {
        "data": [
            {"c": None, "p": 57328.15, "s": "BINANCE:BTCUSDT", "t": 1720504086187, "v": 0.00039},
            {"c": None, "p": 57328.15, "s": "BINANCE:BTCUSDT", "t": 1720504086284, "v": 0.00017}
        ],
        "type": "trade"
    }
    encoded_data = encode(schema=schema, data=example_data)
    print(encoded_data)
    decoded_data = decode(schema=schema, value=encoded_data)
    print(decoded_data)
    