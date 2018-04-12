FROM python:3.5-jessie

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY ./bin/entrypoint.sh /app
COPY . /app

RUN sh entrypoint.sh


EXPOSE 8000


CMD ["gunicorn", "aquas_web.wsgi:application", "--name aquas_web", "--bind 0.0.0.0:8000", "--workers 3"]
# CMD ["python", "aquas_web/manage.py", "runserver", "0.0.0.0:8000"]
