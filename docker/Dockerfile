FROM registry.suse.com/bci/python:3.11
#registry.opensuse.org/opensuse/bci/python:latest

RUN pip install --upgrade pip
COPY ./code /trento-gui
WORKDIR /trento-gui
RUN pip install -r requirements.txt

CMD ["streamlit", "run", "app.py"]

HEALTHCHECK CMD curl -f http://localhost:8501//healthz || exit 1
