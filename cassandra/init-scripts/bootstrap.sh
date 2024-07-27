#!/bin/bash
set -e

/docker-entrypoint.sh "$@" &

# Wait for Cassandra to start
until cqlsh -e "DESCRIBE KEYSPACES"; do
  >&2 echo "Cassandra is unavailable - sleeping"
  sleep 2
done

>&2 echo "Cassandra is up - executing bootstrap script"

# Example: Create a keyspace and insert some data
cqlsh -f /docker-entrypoint-initdb.d/init.cql

>&2 echo "Bootstrap script executed successfully"

# Optionally, you can add more commands here to initialize your database

exit 0
