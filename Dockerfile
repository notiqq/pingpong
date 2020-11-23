# Using a python small basic image
FROM python:alpine
RUN apk update && apk bash build-base python3-dev libffi-dev


EXPOSE 5000
RUN  pip install -r requirements.txt

# Run the application
WORKDIR /ping-pong
CMD python -u master.py