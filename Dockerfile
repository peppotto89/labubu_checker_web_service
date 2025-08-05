# Usa un'immagine Python ufficiale
FROM python:3.11-slim

# Installiamo dipendenze di sistema per Chromium + pyppeteer
RUN apt-get update && apt-get install -y \
    wget \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk1.0-0 \
    libc6 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libexpat1 \
    libfontconfig1 \
    libgbm1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    lsb-release \
    xdg-utils \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Installiamo pyppeteer tramite pip
RUN pip install --no-cache-dir pyppeteer==0.2.6 fastapi uvicorn

# Scarichiamo Chromium per pyppeteer
RUN python -c "from pyppeteer import chromium_downloader; chromium_downloader.download_chromium()"

# Copiamo il codice dell'app nel container
WORKDIR /app
COPY . /app

# Espone la porta che userà uvicorn
EXPOSE 8000

# Comando per avviare l'app (modifica se usi file o comando diverso)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
