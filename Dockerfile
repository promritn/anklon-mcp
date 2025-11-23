FROM python:3.12-slim

WORKDIR /app

# Install curl for healthcheck and openssl for SSL certificates
RUN apt-get update && apt-get install -y curl openssl && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY app_unified.py .
COPY words.json .
COPY KK.json .
COPY prob.txt .
COPY generate_cert.sh .

# Expose port
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Generate self-signed SSL certificate at build time
RUN chmod +x generate_cert.sh && bash generate_cert.sh

# Health check (use -k flag to allow self-signed cert)
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f -k https://localhost:5000/health || curl -f http://localhost:5000/health || exit 1

# Run the unified application
CMD ["python", "-u", "app_unified.py"]
