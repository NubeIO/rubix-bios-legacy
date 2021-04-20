import subprocess


def execute_command_with_exception(cmd, cwd=None):
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, cwd=cwd)
