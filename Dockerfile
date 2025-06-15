FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y ffmpeg git imagemagick && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Clone Pixray repo manually (not installable via pip)
RUN git clone https://github.com/pixray/pixray.git

COPY app.py .

EXPOSE 80

CMD ["python", "app.py"]