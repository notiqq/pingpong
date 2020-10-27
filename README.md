# Ping-pong dockerized app

## Pre-requisites
- Have Docker and Docker Compose installed on the machine. 
- Clone this repo

## How To Build The Images and Launch The Containers
Set into the cloned repo (cd \<repo>)

Run the following command:</br>
``` 
docker-compose up
```
## How To Run This App
Use a URL with the following syntax:
```
http://localhost:[port]/pingpong?iterations=[integer]
```
e.g. Use curl to run it:
```
curl "http://localhost:5001/pingpong?iterations=6"
```
