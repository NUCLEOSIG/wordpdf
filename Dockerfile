FROM python:3.11-slim

# Evita que Python genere archivos .pyc y permite logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instalar dependencias del sistema
# Se incluyen librerías para mysqlclient y xhtml2pdf (pango, cairo, etc.)
RUN apt-get update && apt-get install -y build-essential default-libmysqlclient-dev pkg-config libcairo2 libcairo2-dev pkg-config libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-2.0-0 libffi-dev shared-mime-info libgdiplus libicu-dev && rm -rf /var/lib/apt/lists/*

RUN echo "deb http://deb.debian.org/debian bookworm contrib non-free" > /etc/apt/sources.list.d/contrib.list
RUN apt-get update && apt-get install -y --no-install-recommends ttf-mscorefonts-installer
ENV LD_LIBRARY_PATH=/usr/share/fonts:usr/local/share/fonts

# Instalar dependencias de Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el código del proyecto
COPY . /app/

# Exponer el puerto
EXPOSE 9100

# Comando por defecto (se puede sobrescribir en docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:9100"]