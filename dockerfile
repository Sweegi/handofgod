FROM python:3.6-alpine

WORKDIR /app
COPY ./setup/packages.txt .

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    # && pip3 install -r packages.txt -i https://pypi.mirrors.ustc.edu.cn/simple/ \
    && apk add g++ gcc python3-dev openssl-dev \
    && apk add jpeg-dev zlib-dev \
    && apk add tzdata && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && apk del tzdata
