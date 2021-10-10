FROM python:3

ADD main.py /

RUN mkdir -p images/

RUN pip install requests

RUN pip install boto3

RUN pip install pandas

RUN pip install matplotlib

CMD [ "python", "./main.py" ]