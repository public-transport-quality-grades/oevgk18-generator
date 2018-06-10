FROM python:3.6-stretch

COPY . /src
WORKDIR /src

RUN apt-get update && apt-get install -y libgeos-dev

RUN pip install -r requirements.txt
RUN pip install .

RUN mkdir /generator
WORKDIR /generator

CMD ["/usr/local/bin/oevgk18_generator", "--help"]
