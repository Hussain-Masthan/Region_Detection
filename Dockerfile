FROM python:3.9

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

# Setting Home Directory for containers
WORKDIR /usr/src/app

# Installing python dependencies
COPY /requirements.txt /usr/src/app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copying src code to Container
COPY . /usr/src/app
# Application Environment variables
#ENV APP_ENV development
ENV PORT 8000

# Exposing Ports
EXPOSE $PORT

# Setting Persistent data
#VOLUME ["/app-data"]

# Running Python Application
#CMD gunicorn -b :$PORT -c gunicorn.conf.py main:app

CMD ["python", "app.py"]