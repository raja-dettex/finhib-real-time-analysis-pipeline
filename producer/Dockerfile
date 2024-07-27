FROM python:3.9
WORKDIR /app
COPY ./src/ /app/src
RUN python -m venv /app/venv
RUN . /app/venv/bin/activate 
RUN pip install -r /app/src/requirements.txt


