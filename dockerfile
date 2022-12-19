FROM python:3
MAINTAINER Felix Fleckenstein

WORKDIR /usr/src/app

Copy . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
#CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000"]
CMD ["/bin/bash", "-c", "python ./manage.py migrate;python ./manage.py runserver 0.0.0.0:8000"]