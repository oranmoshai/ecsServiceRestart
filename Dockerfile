FROM python:2.7.15-alpine3.7

RUN apk add --update \
    linux-headers \
    build-base

WORKDIR /opt
ADD / /opt
RUN pip install -r requirements.txt

CMD ["/bin/bash"]
