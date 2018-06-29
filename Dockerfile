FROM python:3.6-alpine3.6 AS spider

ENV APP_DIR $HOME/spider



RUN mkdir -p ${APP_DIR} && mkdir -p ${APP_DIR}/logs
COPY . ${APP_DIR}

WORKDIR ${APP_DIR}
RUN echo 'http://mirrors.aliyun.com/alpine/v3.6/community/'>/etc/apk/repositories \
    && echo 'http://mirrors.aliyun.com/alpine/v3.6/main/'>>/etc/apk/repositories \ 
    && apk add --no-cache tzdata \
    && cp /usr/share/zoneinfo/Asia/Chongqing /etc/localtime \
    && apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev libxslt-dev libxml2-dev \ 
    && pip install -r reqrements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/ 

CMD scrapy crawl lianjia