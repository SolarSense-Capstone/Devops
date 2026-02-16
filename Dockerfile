# Use the official Python 3.11 slim image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy everything from app/ folder
COPY app/ .

# Install dependencies (now requirements.txt is in current directory)
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 8000

# Start the FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]