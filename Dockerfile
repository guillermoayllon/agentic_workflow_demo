# Create a Dockerfile for building an image with Python and data science libraries

# Use the official Ubuntu base image
FROM ubuntu:latest

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && apt-get clean 
# Create a virtual environment
RUN python3 -m venv /venv

# Activate the virtual environment
ENV PATH="/venv/bin:$PATH"

# Install Python data science libraries
RUN pip install --no-cache-dir \
    numpy \
    pandas \
    matplotlib \
    plotly \
    yfinance \
    scipy \
    seaborn\
    scikit-learn

RUN pip install --upgrade pip setuptools


WORKDIR /app

CMD ["python3"]
