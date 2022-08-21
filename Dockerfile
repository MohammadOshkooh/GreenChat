# pull base image
FROM python:3.10

# set envorenment variables
ENV PYTHONDONTWRITEBYTCODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
RUN mkdir /code
WORKDIR /code

## install node js
#RUN apt-get update && apt-get install -y \
#    software-properties-common \
#    npm
#RUN npm install npm@latest -g && \
#    npm install n -g && \
#    n latest

# install dependencies
COPY ./requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/

