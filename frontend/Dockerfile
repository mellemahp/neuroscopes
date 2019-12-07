FROM alpine:3.10.3

# ensures logging is correct
ENV PYTHONUNBUFFERED=1

RUN apk add --update --no-cache \
    python3 \
    python3-dev

# Install all python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt && \
    rm requirements.txt

COPY ./code/ /app/ 
WORKDIR /app/

ENTRYPOINT [ "python3", "frontend.py" ]