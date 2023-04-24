FROM python:3.7.16-buster

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY edbm34_ugc /edbm34_ugc

WORKDIR /edbm34_ugc

CMD ["./bootstrap.sh"]
