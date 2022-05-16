FROM alpine:3.15
ARG TZ='Asia/Tokyo'

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

LABEL maintainer="yuruto"

COPY ./requirements.txt /requirements.txt

RUN    apk update \
    \
    # Install basic libraries and setup timezone
    \
    && apk add --no-cache bash tzdata jq curl \
    && cp /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo ${TZ} > /etc/timezone \
    \
    # install temporary libraries
    \
    && apk add --no-cache --virtual .build-deps \
               gcc musl-dev libffi-dev g++ libgcc libstdc++ python3-dev \
               libc-dev linux-headers openssl-dev \
    \
    # install python3 and pip3
    \
    && apk add --no-cache python3 \
    && python3 -m ensurepip \
    && rm -r /usr/lib/python*/ensurepip \
    && pip3 install --upgrade pip setuptools \
    \
    # create symbolic link
    \
    && ln -sf /usr/bin/python3 /usr/bin/python \
    && ln -sf /usr/bin/pip3 /usr/bin/pip \
    \
    # install python libraries
    \
    && pip install -r /requirements.txt \
    && apk --purge del .build-deps \
    && mkdir /code \
    && rm -rf /root/.cache /var/cache/apk/* /tmp/*

COPY ./wait.py /code/app.py
COPY ./start.sh /start.sh
RUN chmod 777 /start.sh

WORKDIR /code

CMD ["/start.sh"]
