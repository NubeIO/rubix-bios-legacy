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


def systemctl_status(service) -> dict:
    p = subprocess.Popen(["systemctl", "status", service], stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    output = output.decode('utf-8')
    active_status_regx = r"Active:(.*) since (.*);(.*)"
    loaded_status_regx = f"Loaded:(.*); (.*);(.*)"
    service_status = {}
    for line in output.splitlines():
        active_status_search = re.search(active_status_regx, line)
        if active_status_search:
            state = active_status_search.group(1).strip().split(" ")[0]
            service_status['state'] = state
            service_status['status'] = (state == 'active')
            service_status['date_since'] = active_status_search.group(2).strip()
            service_status['time_since'] = active_status_search.group(3).strip()
        loaded_status_search = re.search(loaded_status_regx, line)
        if loaded_status_search:
            service_status['is_enabled'] = loaded_status_search.group(2).strip() == 'enabled'
    return service_status


def systemctl_status_specific_details(service) -> dict:
    p = subprocess.Popen(["systemctl", "status", service], stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    output = output.decode('utf-8')
    active_status_regx = r"Active:(.*) since (.*);(.*)"
    service_status = {}
    for line in output.splitlines():
        active_status_search = re.search(active_status_regx, line)
        if active_status_search:
            service_status['date_since'] = active_status_search.group(2).strip()
            service_status['time_since'] = active_status_search.group(3).strip()
    return service_status


def systemctl_installed(service) -> bool:
    """
    Return True if systemd service is installed
    example: check = systemctl_installed('mosquitto')
    """
    try:
        cmd: str = "systemctl status {} | wc -l | grep -w -Fq 0 && echo FALSE || echo TRUE".format(service)
        completed = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        return False
    for line in completed.stdout.decode('utf-8').splitlines():
        if 'TRUE' in line:
            return True
    return False
