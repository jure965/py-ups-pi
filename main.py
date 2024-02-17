import logging.config
import argparse
import yaml

from pathlib import Path
from typing import Dict

from PyNUTClient.PyNUT import PyNUTClient
from ping3 import ping


with open('logging.yaml', 'rt') as f:
    logging_config = yaml.safe_load(f.read())

logging.config.dictConfig(logging_config)
logger = logging.getLogger('main')


class Host:
    def __init__(self, name, mac, address):
        self.name = name
        self.mac = mac
        self.address = address


def is_alive(host: Host) -> bool:
    return bool(ping(host.address))


def decode_dict(x: Dict) -> Dict:
    return {y.decode('ascii'): x.get(y).decode('ascii') for y in x.keys()}


def main():
    logger.info('Starting application')

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

    hosts = []
    for k, v in config['hosts'].items():
        hosts.append(Host(k, **v))

    nut_server = config['nut_server']
    ups_name = config['ups_name']

    for host in hosts:
        alive = is_alive(host)
        print(f'{host.name=} {host.address=} {alive=}')

    nut_client = PyNUTClient(
        host=nut_server['host'],
        port=nut_server['port'],
        login=nut_server['username'],
        password=nut_server['password'],
    )

    ups_vars = decode_dict(nut_client.GetUPSVars(ups_name))

    battery_charge = int(ups_vars["battery.charge"])
    battery_runtime = int(ups_vars["battery.runtime"])
    ups_status = ups_vars["ups.status"]

    print(f'{battery_charge=} {battery_runtime=} {ups_status=}')


if __name__ == '__main__':
    main()
