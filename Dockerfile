FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir ./files ./files/input ./files/processado ./files/log
COPY . .
CMD ["python3", "cyberleak.py"]