FROM cassandra:latest
COPY ./init-scripts/init.cql /docker-entrypoint-initdb.d/init.cql
EXPOSE  9042
RUN cqlsh -f /docker-entrypoint-initdb.d/init.cql