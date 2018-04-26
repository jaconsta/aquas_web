FROM python:3.5-jessie

RUN mkdir /app
WORKDIR /app

RUN apt-get install libmysqlclient-dev

COPY requirements.txt /app
RUN pip install -r requirements.txt
RUN pip install mysqlclient

COPY ./bin/entrypoint.sh /app
COPY ./aquas_web /app

EXPOSE 8000

CMD ["gunicorn", "aquas_web.wsgi:application", "--name", "aquas_web", "--bind", "0.0.0.0:8000", "--workers", "3"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
