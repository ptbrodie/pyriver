import os

from pyriver.db import db


def write_schema():
    starter = """{
       "metadata": {
            "name": "My River",
            "user": "ptbrodie",
            "interval": "hourly",
            "entry": "MyEntry.py"
       },
       "data": {
            "_comment": "your data here"
       }
    }"""
    with open ("river.json", "w+") as schema:
        schema.writelines(starter)


def write_dockerfile():
    lines = [
        "FROM python:3-onbuild",
        "RUN apt-get update",
        "RUN apt-get -y install postgresql-client-9.4 redis-server",
        "RUN service redis-server start",
        "RUN mkdir -p /usr/src/river",
        "COPY . /usr/src/river/",
        "WORKDIR /usr/src/river",
        "RUN chmod +x run.sh",
        "RUN pip install pyriver",
        "RUN if [ -f $FILE ]; then pip install -r requirements.txt; fi",
        "CMD [ './run.sh' ]"
    ]
    with open(".river/Dockerfile", "w+") as dockerfile:
        dockerfile.writelines(lines)


def write_executable():
    content = [
        "#!/usr/bin/env sh",
        "service redis-server start",
"river run > log.txt"
    ]
    os.makedirs(".river/bin/")
    with open(".river/bin/run", "w+") as executable:
        executable.writelines(content)


def execute():
    os.makedirs(".river/")
    write_schema()
    write_dockerfile()
    write_executable()
    db.initdb()
