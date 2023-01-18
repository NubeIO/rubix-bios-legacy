# CHANGELOG
## [v1.8.0](https://github.com/NubeIO/rubix-bios/tree/v1.8.0) (2023-01-18)
### For k8s
- Add OpenVPN on the default image & add a CRON config copier

## [v1.7.0](https://github.com/NubeIO/rubix-bios/tree/v1.7.0) (2023-01-13)
### For k8s
- CRON backup `/lib/system/system/nubeio-*` to `/data/system/system/`

## [v1.6.0](https://github.com/NubeIO/rubix-bios/tree/v1.6.0) (2023-01-10)
### For k8s
- Fix: pyintaller upgrade for build failure
- Add rubix-edge-bios so it start with those two default BIOS

## [v1.5.3](https://github.com/NubeIO/rubix-bios/tree/v1.5.3) (2021-11-15)
### For k8s
- Docker image build improvement

## [v1.5.2](https://github.com/NubeIO/rubix-bios/tree/v1.5.2) (2020-07-09)
- Improvement on restart command

## [v1.5.1](https://github.com/NubeIO/rubix-bios/tree/v1.5.1) (2020-06-30)
- Block background check iteration on blocked state

## [v1.5.0](https://github.com/NubeIO/rubix-bios/tree/v1.5.0) (2020-06-24)
- Use registry for GitHub token
- Add Gunicorn, gevent for running the app
- Add self upgrade, app service API
- Expose APIs for local apps without authorization
- Restrict downgrade rubix-service
- Wait background status get process on restarting
- Include token on commandline

## [v1.4.1](https://github.com/NubeIO/rubix-bios/tree/v1.4.1) (2020-05-27)
- Issue fix: str' object has no attribute 'get'

## [v1.4.0](https://github.com/NubeIO/rubix-bios/tree/v1.4.0) (2020-04-20)
- Create service control API for start, stop, restart, enable, disable rubix-service

## [v1.3.0](https://github.com/NubeIO/rubix-bios/tree/v1.3.0) (2020-03-21)
- Change default password
- Update rubix-service from artifacts option (an alternative of upgrade Rubix Service)

## [v1.2.0](https://github.com/NubeIO/rubix-bios/tree/v1.2.0) (2020-03-03)
- Add root directory for rubix-service

## [v1.1.0](https://github.com/NubeIO/rubix-bios/tree/v1.1.0) (2020-02-28)
- Auth implementation
- Data, Config & Apps directory standardization

## [v1.0.0](https://github.com/NubeIO/rubix-bios/tree/v1.0.0) (2020-01-27)
- Additional APIs for installing latest or selected version of rubix-service

## [v1.0.0-rc.1](https://github.com/NubeIO/rubix-bios/tree/v1.2.0-rc.1) (2020-01-20)
- First ever successful release