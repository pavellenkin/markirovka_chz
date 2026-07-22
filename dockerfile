# Используем официальный Python образ
FROM python:3.12

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*



   

# Устанавливаем рабочую директорию
WORKDIR /

ENV PYTHONPATH=/

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn whitenoise

# Копируем весь проект
COPY . .

# Устанавливаем все deb пакеты из pycades_requirements
RUN dpkg -i pycades_requirements/*.deb 2>/dev/null; exit 0 && \
    apt-get update && apt-get install -f -y && \
    apt-get clean

RUN python manage.py collectstatic --noinput

# Открываем порт
EXPOSE 9797

# Создаём entrypoint скрипт для запуска обоих процессов
RUN echo '#!/bin/bash\n\
# Запуск cryptsrv в фоне\n\
/opt/cprocsp/sbin/amd64/cryptsrv &\n\
# Ожидание инициализации\n\
sleep 3\n\
# Запуск gunicorn\n\
exec gunicorn --bind 0.0.0.0:9797 \\\n\
    --workers 3 \\\n\
    --access-logfile - \\\n\
    --error-logfile - \\\n\
    --log-level info \\\n\
    NationalCatalogParse.wsgi:application' > /entrypoint.sh && \
chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]