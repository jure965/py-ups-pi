import logging.config
import argparse

import yaml
import asyncio

from pathlib import Path

from classes import Host, WakeConfig, UPSStatus
from host_monitor import host_monitor
from ups_monitor import ups_monitor

with open('logging.yaml', 'rt') as f:
    logging_config = yaml.safe_load(f.read())

logging.config.dictConfig(logging_config)

logger = logging.getLogger('main')


async def main():
    parser = argparse.ArgumentParser(
        prog='pyupspi',
        description='Monitor NUT server and wake machines based on UPS battery level.',
    )
    parser.add_argument(
        '-c', '--config', default='config.yaml', required=False
    )
    args = parser.parse_args()

    if not Path(args.config).is_file():
        logger.critical(f'Config file not found: {args.config}')
        exit(1)

    with open(args.config, 'rt') as c:
        config = yaml.safe_load(c.read())

    hosts = [Host(**host) for host in config['hosts']]

    nut_server = config['nut_server']
    ups_name = config['ups_name']

    wake_config = WakeConfig(**config['wake_on'])
    ups_status = UPSStatus(0, 0, 'UNKNOWN')

    tasks = [asyncio.create_task(ups_monitor(nut_server, ups_name, ups_status))]

    for host in hosts:
        tasks.append(asyncio.create_task(host_monitor(host, wake_config, ups_status)))

    logger.info('Application started')

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Application shut down complete')
