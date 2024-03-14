FROM python:3-slim

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED=1

COPY . .

RUN python -m pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]