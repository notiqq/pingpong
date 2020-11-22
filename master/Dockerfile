# Using a python small basic image
FROM python:alpine

# Install git
RUN apk add --no-cache git
EXPOSE 5000
# Copy repo and install dependencies
RUN git clone https://github.com/drorle/ping-pong.git ;\
    cd /ping-pong ;\
    pip install -r requirements.txt 

# Run the application
WORKDIR /ping-pong
CMD python -u pingpong.py