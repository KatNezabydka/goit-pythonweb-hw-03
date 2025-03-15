# Docker-команда FROM вказує базовий образ контейнера
# Наш базовий образ - це Linux з попередньо встановленим python-3.10
# Краще використовувати python:3.10-alpine3.20, оскільки він має менший розмір
# REPOSITORY    TAG       IMAGE ID       CREATED          SIZE
# tiog          0.1.0     60746a585e65   14 seconds ago   1.02GB  <-- python:3.10
# tiog          0.2.0     36cd2ac84e5a   5 seconds ago    164MB   <-- python:3.10-slim
# tiog          0.3.0     2f3eaff77076   9 seconds ago    67.8MB  <-- python:3.10-alpine3.20
FROM python:3.10-alpine3.20

# Встановимо змінну середовища
ENV APP_HOME=/app

# Встановимо робочу директорію всередині контейнера
WORKDIR $APP_HOME

# Скопіюємо інші файли в робочу директорію контейнера
COPY . .

# Позначимо порт, де працює застосунок всередині контейнера
EXPOSE 3000

# Запустимо наш застосунок всередині контейнера
ENTRYPOINT ["python", "main.py"]
