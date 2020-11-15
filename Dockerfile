FROM python:3.7.2
COPY ./requirements.txt /code/

RUN apt-get update
RUN apt-get install -y libxml2-dev libxmlsec1-dev libxmlsec1-openssl \
    && apt-get install -y netcat sqlite3
RUN pip install -r /code/requirements.txt

COPY ./run.sh /code/run.sh

COPY . /code/
WORKDIR /code

RUN chmod a+x /code/run.sh
CMD /code/run.sh