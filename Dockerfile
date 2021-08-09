FROM python:3.8-slim-buster
RUN apt update && apt -y install python3-tk procps
RUN mkdir -p app
WORKDIR /app
COPY . .
VOLUME ["/app"]
ENTRYPOINT ["./main.py"]
