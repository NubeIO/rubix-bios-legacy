import os
from abc import ABC, abstractmethod

from src.pyinstaller import resource_path
from src.system.utils.file import delete_file
from src.system.utils.shell import execute_command

SERVICE_DIR = '/lib/systemd/system'
SERVICE_DIR_SOFT_LINK = '/etc/systemd/system/multi-user.target.wants'


class Systemd(ABC):
    def __init__(self, service_file_name):
        self.__service_file_name = service_file_name
        self.__service_file = os.path.join(SERVICE_DIR, self.__service_file_name)
        self.__symlink_service_file = os.path.join(SERVICE_DIR_SOFT_LINK, self.__service_file_name)

    def install(self) -> bool:

        print('Creating Linux Service...')
        lines = self.create_service()
        with open(self.__service_file, "w") as file:
            file.writelines(lines)

        print('Soft Un-linking Linux Service...')
        try:
            os.unlink(self.__symlink_service_file)
        except FileNotFoundError as e:
            print(str(e))

        print('Soft Linking Linux Service...')
        os.symlink(self.__service_file, self.__symlink_service_file)

        print('Hitting daemon-reload...')
        if not execute_command('sudo systemctl daemon-reload'):
            return False

        print('Enabling Linux Service...')
        if not execute_command('sudo systemctl enable {}'.format(self.__service_file_name)):
            return False

        print('Starting Linux Service...')
        if not execute_command('sudo systemctl restart {}'.format(self.__service_file_name)):
            return False

        print('Successfully started service')
        return True

    def uninstall(self) -> bool:
        print('Stopping Linux Service...')
        if not execute_command('systemctl stop {}'.format(self.__service_file_name)):
            return False

        print('Un-linking Linux Service...')
        try:
            os.unlink(self.__symlink_service_file)
        except FileNotFoundError as e:
            print(str(e))

        print('Removing Linux Service...')
        delete_file(self.__service_file)

        print('Hitting daemon-reload...')
        if not execute_command('sudo systemctl daemon-reload'):
            return False
        print('Service is deleted.')
        return True

    @abstractmethod
    def create_service(self):
        raise NotImplementedError('Need to be implemented')


class RubixServiceSystemd(Systemd):
    SERVICE_FILE_NAME = 'nubeio-rubix-service.service'

    def __init__(self, wd=None, token=None, device_type=None):
        self.__wd = wd
        self.__token = token
        self.__device_type = device_type
        self.__port = 1515
        self.__data_dir = '/data/rubix-service'
        self.__global_dir = '/data'
        self.__artifact_dir = '/data/rubix-service/apps'
        super().__init__(RubixServiceSystemd.SERVICE_FILE_NAME)

    def create_service(self):
        lines = []
        with open(resource_path('systemd/nubeio-rubix-service.service')) as systemd_file:
            for line in systemd_file.readlines():
                if '<working_dir>' in line and self.__wd:
                    line = line.replace('<working_dir>', self.__wd)
                if '<port>' in line and self.__port:
                    line = line.replace('<port>', str(self.__port))
                if '<data_dir>' in line and self.__data_dir:
                    line = line.replace('<data_dir>', self.__data_dir)
                if '<global_dir>' in line and self.__global_dir:
                    line = line.replace('<global_dir>', self.__global_dir)
                if '<artifact_dir>' in line and self.__artifact_dir:
                    line = line.replace('<artifact_dir>', self.__artifact_dir)
                if ' --token <token>' in line:
                    token = self.__token
                    line = line.replace(' --token <token>', '' if not token else ' --token {}'.format(token))
                if '<device_type>' in line and self.__device_type:
                    line = line.replace('<device_type>', self.__device_type)
                lines.append(line)
        return lines
