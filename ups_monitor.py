import asyncio
import logging
from typing import Dict

from PyNUTClient.PyNUT import PyNUTClient

from classes import UPSStatus


logger = logging.getLogger("ups_monitor")


def decode_dict(x: Dict) -> Dict:
    return {y.decode('ascii'): x.get(y).decode('ascii') for y in x.keys()}


async def ups_monitor(nut_server: Dict, ups_name: str, ups_status: UPSStatus):
    try:
        logger.info(f'UPS monitor started {ups_name=}')
        nut_client = PyNUTClient(
            host=nut_server['host'],
            port=nut_server['port'],
            login=nut_server['username'],
            password=nut_server['password'],
        )
        while True:
            ups_vars = decode_dict(nut_client.GetUPSVars(ups_name))

            ups_status.battery_charge = int(ups_vars["battery.charge"])
            ups_status.battery_runtime = int(ups_vars["battery.runtime"])
            ups_status.ups_status_str = ups_vars["ups.status"]

            logger.info(f'UPS status fetched {ups_name=}')

            await asyncio.sleep(5)
    except asyncio.CancelledError:
        logger.info(f'UPS monitor stopped {ups_name=}')
