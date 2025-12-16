FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create user
RUN useradd -m -u 1000 user
USER user

ENV PATH="/home/user/.local/bin:$PATH"
WORKDIR /app

# Copy requirements
COPY --chown=user requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY --chown=user . /app

# Hugging Face Spaces expects the application to run on port 7860
EXPOSE 7860

# Start the application, using the PORT environment variable if available
# Hugging Face Spaces will set the PORT environment variable
CMD ["sh", "-c", "python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-7860}"]
