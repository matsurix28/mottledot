FROM python:3.11.6-slim

RUN apt-get update && \
    apt-get install --no-install-recommends -y libgl1-mesa-dev \
    libglib2.0-0

RUN pip install opencv-python