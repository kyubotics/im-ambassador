FROM python:3.6.0-alpine
MAINTAINER Richard Chien <richardchienthebest@gmail.com>

COPY *.py ./
COPY filters filters
COPY msg_src_adapters msg_src_adapters
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python app.py