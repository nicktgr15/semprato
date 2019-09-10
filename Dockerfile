FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install python3-pip -y

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY edbm34_ugc /edbm34_ugc

WORKDIR /edbm34_ugc

CMD ["./bootstrap.sh"]
