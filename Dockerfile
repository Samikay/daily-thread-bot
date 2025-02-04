FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code dan environment variables
COPY src/ ./src/
COPY .env .

CMD ["python", "-u", "./src/bot.py"]