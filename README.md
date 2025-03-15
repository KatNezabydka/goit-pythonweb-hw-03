# Message blog

## Prerequisites

Before you start, make sure you have:

- [pyenv](https://github.com/pyenv/pyenv) is installed
- [docker](https://www.docker.com/) is installed

## Installation


### 2. **Create a virtual environment**:
```bash
make setup
```

### 3. **Activate the virtual environment**:
```bash
source venv/bin/activate
```

### 4. **Run the http server and open [http://127.0.0.1:8000](http://127.0.0.1:8000)**:
```bash
# Press Ctrl+C to stop the app
python main.py
```

## Docker

### 1. **Build**:
```bash
docker compose build
```

### 3. **Run**:
```bash
docker compose up -d
```