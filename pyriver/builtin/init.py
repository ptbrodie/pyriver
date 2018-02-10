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
        "FROM python:3-onbuild\n",
        "RUN apt-get update\n",
        "RUN apt-get -y install postgresql-client-9.4 redis-server\n",
        "RUN service redis-server start\n",
        "RUN mkdir -p /usr/src/river\n",
        "COPY . /usr/src/river/\n",
        "WORKDIR /usr/src/river\n",
        "RUN chmod +x run.sh\n",
        "RUN pip install pyriver\n",
        "RUN if [ -f $FILE ]; then pip install -r requirements.txt; fi\n",
        "CMD [ './run.sh' ]\n"
    ]
    with open(".river/Dockerfile", "w+") as dockerfile:
        dockerfile.writelines(lines)


def write_executable():
    content = [
        "#!/usr/bin/env sh\n",
        "service redis-server start\n",
        "river run > log.txt\n"
    ]
    os.makedirs(".river/bin/")
    with open(".river/bin/run", "w+") as executable:
        executable.writelines(content)


def execute():
    if os.path.exists(".river/"):
        exit("A river has already been initialized.")
    os.makedirs(".river/")
    write_schema()
    write_dockerfile()
    write_executable()
    db.initdb()
