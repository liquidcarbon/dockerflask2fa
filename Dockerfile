FROM python:3.8.5-slim-buster
MAINTAINER liquidcarbon

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app
# COPY ./private /private

CMD [ "python", "-c", "import os; print(os.environ)" ]
