FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV FLASK_APP=run.py

EXPOSE 80

CMD ["python", "run.py"]
