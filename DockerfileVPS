FROM python:3.12-slim

WORKDIR /app

# Install system dependencies including ffmpeg and pandoc
RUN apt-get update && \
    apt-get install -y curl ffmpeg pandoc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install PyTorch CPU version first
RUN pip install torch==2.3.0+cpu torchvision==0.18.0+cpu --index-url https://download.pytorch.org/whl/cpu

# Then install the rest of the requirements
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK --interval=5s --timeout=5s --start-period=60s \
  CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app.py", \
            "--server.port=8501", \
            "--server.address=0.0.0.0", \
            "--browser.gatherUsageStats=false", \
            "--server.enableStaticServing=true", \
            "--client.toolbarMode=viewer", \
            "--server.headless=true", \
            "--server.fileWatcherType=none"]