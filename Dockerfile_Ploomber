FROM continuumio/miniconda3

WORKDIR /srv

COPY requirements.txt /srv/

RUN apt-get update && apt-get install ffmpeg pandoc -y

# Use an available version of torchvision
RUN pip install torch==2.3.0+cpu torchvision==0.18.0+cpu --index-url https://download.pytorch.org/whl/cpu
RUN pip install -r requirements.txt --no-cache-dir

COPY . /srv

ENTRYPOINT ["streamlit", "run", "app.py", \
            "--server.port=80", \
            "--server.headless=true", \
            "--server.address=0.0.0.0", \
            "--browser.gatherUsageStats=false", \
            "--server.enableStaticServing=true", \
            "--server.fileWatcherType=none", \
            "--client.toolbarMode=viewer"]