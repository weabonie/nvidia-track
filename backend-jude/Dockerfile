FROM python:3.12

COPY requirements.txt . 
RUN apt update 
RUN apt install -y git gcc
RUN apt install python3-venv -y
RUN python -m venv /opt/venv
RUN /opt/venv/bin/pip install -r requirements.txt

COPY . /opt/app

CMD ["/opt/venv/bin/python", "main.py"]
