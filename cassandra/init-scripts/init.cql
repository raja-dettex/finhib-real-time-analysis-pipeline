-- Create keyspace if not exists
CREATE KEYSPACE IF NOT EXISTS crypto_trades
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

-- Use the keyspace
USE crypto_trades;

-- Create table if not exists
CREATE TABLE IF NOT EXISTS trade_data (
    id UUID PRIMARY KEY,
    price DOUBLE,
    symbol TEXT,
    timestamp TIMESTAMP,
    volume DOUBLE
);
