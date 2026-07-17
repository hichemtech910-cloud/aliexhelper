FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUTF8=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY scraper.py .
CMD ["python", "-u", "scraper.py"]
