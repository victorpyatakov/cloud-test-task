FROM python:3.7

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/

RUN pip install  -r requirements.txt

EXPOSE 5005

CMD ["python","app.py"]