
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64 \
    PATH="/usr/lib/jvm/java-21-openjdk-amd64/bin:${PATH}" \
    PYSPARK_SUBMIT_ARGS="--driver-memory 2g pyspark-shell"

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends openjdk-21-jre-headless \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY tests/ ./tests/
COPY oil_gas_analytics/ ./oil_gas_analytics/
COPY data/silver/ ./data/silver/
COPY data/gold/ ./data/gold/

CMD ["python", "-m", "pytest", "-v", "--ignore=tests/test_spark_silver.py"]
