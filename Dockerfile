FROM python:3.10-slim

# Install Git
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5678

CMD ["python", "your_script.py"]