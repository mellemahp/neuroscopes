FROM debian:bullseye-slim

# ensures logging is correct
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    python3 \
    python3-dev \
    python3-pip \
    libsm6 \
    libxext6 \
    libxrender-dev

COPY requirements.txt .
RUN pip3 install -r requirements.txt && \
    rm requirements.txt

COPY ./code/ /app/ 
WORKDIR /app/

ENTRYPOINT [ "python", "/app/pictureGen.py" ]
