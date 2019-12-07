FROM alpine:3.10.3

# ensures logging is correct
ENV PYTHONUNBUFFERED=1

RUN apk add --update --no-cache \
    npm \ 
    python3 \
    python3-dev && \ 
    ln -sf python3 /usr/bin/python3

# Install all node dependencies
WORKDIR /
COPY package.json webpack.config.js ./
RUN npm install 

# Install all python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt && \
    rm requirements.txt

COPY ./code/ /frontend/app/ 

ENTRYPOINT [ "python", "/app/frontend.py" ]