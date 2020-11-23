FROM python:alpine

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

EXPOSE 5001

RUN pip install -r requirements.txt

WORKDIR /ping-pong

CMD python -u pingpong.py

COPY . /ping-pong

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]