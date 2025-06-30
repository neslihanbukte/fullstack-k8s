FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
RUN mkdir -p /data
COPY data.db /data/data.db
EXPOSE 5000
CMD ["python3", "app/app.py"]