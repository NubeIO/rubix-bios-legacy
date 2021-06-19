import re
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


def systemctl_is_active_service_state(service) -> bool:
    p = subprocess.Popen(["systemctl", "status", service], stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    output = output.decode('utf-8')
    active_status_regx = r"Active:(.*) since (.*);(.*)"
    state: str = ""
    for line in output.splitlines():
        active_status_search = re.search(active_status_regx, line)
        if active_status_search:
            state = active_status_search.group(1).strip().split(" ")[0]
    return state == "active"
