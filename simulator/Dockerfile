FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    curl \
    libcurl4-openssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY . /workspace

RUN cmake -S . -B build && cmake --build build

CMD ["./build/f1_telemetry_simulator", "--config", "config/default.ini", "--mode", "live"]
