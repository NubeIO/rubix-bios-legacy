import subprocess


def execute_command(cmd, cwd=None):
    """Run command line"""
    try:
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, cwd=cwd)
    except subprocess.CalledProcessError:
        return False
    return True


def execute_command_with_exception(cmd, cwd=None):
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, cwd=cwd)
