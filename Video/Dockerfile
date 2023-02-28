FROM python:3.9

WORKDIR /app

#COPY ./requirements.txt .

#COPY ./ .

#RUN pip3 install -r requirements.txt


#FROM python:3.7-alpine

COPY ./ /app

RUN pip3 install -r requirements.txt


ENV TG_TOKEN='5876734711:AAEuAXxnxjF31z-_bPZAxNRrOaOzfdOjb6M'

CMD [ "python3",  "main.py"]