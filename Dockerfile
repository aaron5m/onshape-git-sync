FROM python:3.12-slim

# Set base working directory
WORKDIR /app

# Copy dependencies list
COPY requirements.txt .

# Copy environment
COPY onsync.env .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy scripts directory into the container
COPY scripts/ scripts/

# Move into scripts directory
WORKDIR /app/scripts

# Run the sync script
CMD ["python", "on_sync.py"]
