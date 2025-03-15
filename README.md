# Tiog

This project will contain all code base related to the lectures.


## Prerequisites

Before you start, make sure you have:

- [pyenv](https://github.com/pyenv/pyenv) is installed
- [docker](https://www.docker.com/) is installed

## Installation

### 1. **Clone the repository**:
```bash
git clone https://gitlab.com/vdyshlevyi/tiog
cd tiog
git checkout lecture_3
```

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


## Tests

### 1. **Run tests via**:
```bash
make test
# or
pytest
```

### 2. **Check tests coverage**:
```bash
make coverage
# or
poetry run coverage run --source="." -m pytest -vv
poetry run coverage xml
poetry run coverage report -m --fail-under=5.00
```
