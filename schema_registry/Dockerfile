FROM python:3.9
RUN mkdir -p /temp/script
COPY ./schema.avsc /temp/script/schema.avsc
COPY ./requirements.txt /temp/script/requirements.txt
COPY ./create-schema.py /temp/script/create-schema.py
RUN cd /temp/script
RUN python3 -m venv venv \
    && . ./venv/bin/activate               
RUN pip install -r /temp/script/requirements.txt
