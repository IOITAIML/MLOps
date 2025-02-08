FROM python:3.12-slim
LABEL maintainer="MLOPS"
LABEL version="1.0"

# Fix typo in ENV variable
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy necessary files
COPY ./requirements.txt /requirements.txt
COPY ./models/models.joblib /models/models.joblib
COPY ./webapp/ /app/webapp

# Expose the application port
EXPOSE 8000

# Install required dependencies
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt && \
    rm -rf /root/.cache && \
    adduser --disabled-password --no-create-home appuser

# Set the environment path
ENV PATH="/py/bin:$PATH"

# Switch to non-root user
USER appuser
