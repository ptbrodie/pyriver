import subprocess


def execute():
    subprocess.call(["docker", "build", ".", "--file", ".river/Dockerfile"])
