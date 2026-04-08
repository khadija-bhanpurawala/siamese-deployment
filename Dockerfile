# Use a lightweight Python 3.10 image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the required port
EXPOSE 5000

# Run the application using Gunicorn for production
CMD ["gunicorn", "--workers", "1", "--threads", "1", "--timeout", "180", "--preload", "-b", "0.0.0.0:5000", "app:app"]