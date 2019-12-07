FROM alpine:3.10.3

# ensures logging is correct
ENV PYTHONUNBUFFERED=1

RUN apk add --update --no-cache \
    python3 \
    python3-dev && \ 
    ln -sf python3 /usr/bin/python3

COPY requirements.txt .
RUN pip3 install -r requirements.txt && \
    rm requirements.txt

COPY ./code/ /app/ 

ENTRYPOINT [ "python", "/app/pictureGen.py" ]