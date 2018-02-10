import subprocess


def execute():
    subprocess.popen(["docker", "build", ".", "--file", ".river/Dockerfile"])
