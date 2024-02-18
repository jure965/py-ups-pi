import asyncio
import logging

import wakeonlan
from ping3 import ping

from classes import Host, WakeConfig, UPSStatus


logger = logging.getLogger("host_monitor")


def is_alive(host: Host) -> bool:
    return bool(ping(host.address))


async def host_monitor(host: Host, wake_config: WakeConfig, ups_status: UPSStatus):
    try:
        logger.info(f'Host monitor started {host.name=}')
        while True:
            await asyncio.sleep(5)

            if ups_status.ups_status_str == "UNKNOWN":
                logger.info(f'UPS status {ups_status.ups_status_str}')
                continue

            if ups_status.ups_status_str == wake_config.ups_status_str \
                    and ups_status.battery_charge >= wake_config.batt_level_gte \
                    and ups_status.battery_runtime >= wake_config.runtime_gte:
                if not is_alive(host):
                    wakeonlan.send_magic_packet(host.mac)
                    logger.info(f'Sent magic packet {host.name=}')
                else:
                    logger.info(f'Host is alive {host.name=}')
            else:
                logger.info(f'UPS conditions not met for wake up call')

    except asyncio.CancelledError:
        logger.info(f'Host monitor stopped {host.name=}')
