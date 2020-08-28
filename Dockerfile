FROM python:3.8.5-slim-buster
MAINTAINER liquidcarbon

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
# RUN apk add --update --no-cache --virtual .tmp-build-deps gcc g++
RUN pip install -r /requirements.txt
# RUN apk del .tmp-build-deps
# RUN adduser --system pyuser --shell /bin/bash && su pyuser

RUN mkdir /app /data
WORKDIR /app
COPY ./app /app
COPY ./data /data

CMD [ "python", "-c", "import os; print(os.environ)" ]
