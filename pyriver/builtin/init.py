import os

from pyriver.api import create_app
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
        "RUN apt-get -y install postgresql-client-9.4 sqlite3 redis-server\n",
        "RUN mkdir -p /usr/src/river\n",
        "COPY . /usr/src/river/\n",
        "WORKDIR /usr/src/river\n",
        "RUN chmod 0777 /usr/src/river/.river/bin/run\n",
        "RUN pip install -e file:///usr/src/river/venv/src/pyriver#egg=pyriver --upgrade\n",
        "RUN if [ -f $FILE ]; then pip install -r requirements.txt; fi\n",
        "ENV RIVER_HOME /usr/src/river/\n",
        "CMD [ \"/usr/src/river/.river/bin/run\" ]\n"
    ]
    with open(".river/Dockerfile", "w+") as dockerfile:
        dockerfile.writelines(lines)


def write_executable():
    content = [
        "#!/bin/sh\n",
        "service redis-server start\n",
        "cd /usr/src/river\n",
        "river-server &\n",
        "river run\n"
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
    db.create_all()
