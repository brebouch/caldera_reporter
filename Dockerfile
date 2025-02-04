# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . /app

# Install dependencies
# Install dependencies
RUN apt-get update && apt-get install -y curl \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean



# Expose ports
EXPOSE 5005

# Run the Flask app using Gunicorn
CMD ["sh", "-c", "gunicorn app:app -c gunicorn_config.py"]