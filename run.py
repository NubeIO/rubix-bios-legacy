#!/usr/bin/env python3

import os

import click

from src.app import create_app
from src.service.systemd import RubixBiosSystemd
from src.setting import AppSetting

CLI_CTX_SETTINGS = dict(help_option_names=["-h", "--help"], max_content_width=120)


@click.command(context_settings=CLI_CTX_SETTINGS)
@click.option('-p', '--port', type=int, default=AppSetting.PORT, show_default=True, help='Port')
@click.option('-g', '--global-dir', type=click.Path(), default=lambda: os.environ.get(AppSetting.GLOBAL_DATA_DIR_ENV),
              help='Global data dir')
@click.option('-d', '--data-dir', type=click.Path(), default=lambda: os.environ.get(AppSetting.DATA_DIR_ENV),
              help='Application data dir')
@click.option('-c', '--config-dir', type=click.Path(), default=lambda: os.environ.get(AppSetting.CONFIG_DIR_ENV),
              help='Application config dir')
@click.option('-a', '--artifact-dir', type=click.Path(), default=lambda: os.environ.get(AppSetting.ARTIFACT_DIR_ENV),
              help='Artifact downloaded dir')
@click.option('--prod', is_flag=True, help='Production mode')
@click.option('--device-type', type=click.Choice(['amd64', 'arm64', 'armv7']), default='armv7', show_default=True,
              help='Device type')
@click.option('--install', is_flag=True, help='Install rubix-bios')
@click.option('--uninstall', is_flag=True, help='Uninstall rubix-bios')
@click.option('--auth', is_flag=True, help='Enable JWT authentication')
def cli(port, global_dir, data_dir, config_dir, artifact_dir, prod, device_type, install, uninstall, auth):
    setting = AppSetting(global_dir=global_dir, data_dir=data_dir, config_dir=config_dir, artifact_dir=artifact_dir,
                         prod=prod, device_type=device_type, auth=auth)

    if install:
        systemd = RubixBiosSystemd(os.getcwd(), setting.device_type, setting.auth)
        systemd.install()
    elif uninstall:
        systemd = RubixBiosSystemd()
        systemd.uninstall()
    else:
        app = create_app(setting)
        app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    cli()
