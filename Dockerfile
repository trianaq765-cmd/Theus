# Gunakan Python slim version
FROM python:3.9-slim

# Update linux package list dan install Lua 5.1
# Kita tambahkan --no-install-recommends agar ringan
RUN apt-get update && \
    apt-get install -y lua5.1 && \
    rm -rf /var/lib/apt/lists/*

# Set folder kerja
WORKDIR /app

# Buat user non-root (Keamanan standar untuk HuggingFace/Koyeb)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Copy file requirements dulu (untuk cache)
COPY --chown=user requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy sisa file project
COPY --chown=user . .

# Buka port 7860 (HuggingFace default port 7860, Render/Koyeb biasanya detect otomatis)
EXPOSE 7860

# Jalankan Gunicorn
# Timeout diperpanjang jaga-jaga proses obfuscate lama
CMD ["gunicorn", "-b", "0.0.0.0:7860", "--timeout", "120", "app:app"]