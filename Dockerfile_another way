FROM python:3.12-slim

EXPOSE 8000

WORKDIR /myapp

MAINTAINER vidyasree


COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . . 

CMD ["python" , "app.py"]





