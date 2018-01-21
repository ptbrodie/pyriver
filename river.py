import sys

from builtin import init
from builtin import run


def load():
    pass


def pull():
    pass


def push():
    pass


def backfill():
    pass


commands = {
    "init": init.execute,
    "load": load,
    "run": run.execute,
    "pull": pull,
    "push": push,
    "backfill": backfill
}


if __name__ == "__main__":
    from client.db import db
    commands[sys.argv[1]]()
