# Use a base image with Python
FROM python:3.9

# Install Java (required for PySpark)
RUN apt-get update && \
    apt-get install -y default-jdk && \
    apt-get clean

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code intuit_final.py
COPY intuit_final.py /app/intuit_final.py
WORKDIR /app

# Expose the FastAPI port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "intuit_final:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
