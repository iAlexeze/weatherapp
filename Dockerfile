# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /weatherapp

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port (optional, defaults to 8080 if not provided)
EXPOSE 8080

# Run Gunicorn, using PORT from environment variable (default 8080)
CMD ["sh", "-c", "gunicorn -w 4 -b 0.0.0.0:${PORT:-8080} weatherapp:app"]