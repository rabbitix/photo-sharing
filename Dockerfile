FROM python:3.11-alpine
RUN mkdir /app
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r ./requirements.txt
COPY manage.py .
COPY main.py .
COPY index.html .
COPY src ./src
