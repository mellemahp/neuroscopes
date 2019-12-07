FROM debian:bullseye-slim

# ensures logging is correct
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    python3 \
    python3-dev \
    python3-pip

COPY requirements.txt .
RUN pip3 install -r requirements.txt && \
    rm requirements.txt

COPY ./code/ /app/
WORKDIR /app/

ENTRYPOINT [ "python3", "horoscopeGen.py" ]