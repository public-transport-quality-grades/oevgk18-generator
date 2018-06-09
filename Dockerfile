FROM python:3.6-stretch

COPY . /oevgk18-generator
WORKDIR /oevgk18-generator

RUN apt-get update && apt-get install -y libgeos-dev

RUN pip install -r requirements.txt
RUN pip install .

ENTRYPOINT ["/usr/local/bin/oevgk18_generator"]
CMD ["--help"]
