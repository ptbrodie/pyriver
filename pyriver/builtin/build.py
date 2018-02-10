import subprocess


def execute():
    subprocess.Popen(["docker", "build", ".", "--file", ".river/Dockerfile"])
