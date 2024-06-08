FROM python:3.11-bullseye

ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PATH=$PATH:/home/flaskapp/.local/bin

RUN useradd --create-home --home-dir /home/flaskapp flaskapp

WORKDIR /home/flaskapp

USER flaskapp
RUN mkdir app

COPY ./app ./app
COPY ./app.py .

ADD requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gevent gunicorn==22.0.0

EXPOSE 5000

CMD ["gunicorn", "--workers", "1", "--log-level", "INFO", "--bind", "0.0.0.0:5000", "app:create_app()"]