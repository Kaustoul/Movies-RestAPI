FROM python:3.10.12-alpine

COPY db.py /app/db.py
COPY main.py /app/main.py
COPY movie.py /app/movie.py
COPY requirements.txt /app/requirements.txt
COPY test.py /app/test.py

WORKDIR /app

RUN pip install -r requirements.txt

ENV FLASK_APP=main.py
ENV FLASK_ENV=development

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]