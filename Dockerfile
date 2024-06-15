FROM python:3.9-slim

WORKDIR /app

copy requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./src /app/src
ENV PYTHONPATH "${PYTHONPATH}:/app/src"

CMD ["python", "src/app.py"]
