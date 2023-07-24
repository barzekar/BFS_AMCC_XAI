# Use a slim Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy local code to the container
COPY . .

# Install required packages
# Cleaning up cache to reduce layer size
RUN pip install -r requirements.txt && rm -rf /root/.cache

# Document the port your app listens on
# EXPOSE 5000

# Default command to run
CMD ["python", "app.py"]
