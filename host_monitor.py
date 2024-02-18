import asyncio
import logging
from datetime import timedelta, datetime

import wakeonlan
from ping3 import ping

from classes import Host, WakeConfig, UPSStatus

logger = logging.getLogger("host_monitor")


def is_alive(host: Host) -> bool:
    return bool(ping(host.address))


async def host_monitor(host: Host, wake_config: WakeConfig, ups_status: UPSStatus):
    try:
        logger.info(f'Host monitor started {host.name=}')
        last_wake = datetime.now()
        while True:
            await asyncio.sleep(5)
            now = datetime.now()

            if ups_status.status == "UNKNOWN":
                logger.info(f'UPS status {ups_status.status}')
                continue

            if not (ups_status.status == wake_config.status
                    and ups_status.charge >= wake_config.charge
                    and ups_status.runtime >= wake_config.runtime):
                logger.info(f'UPS conditions not met for wake up call')
                continue

            alive = is_alive(host)
            can_wake = last_wake < now - timedelta(seconds=wake_config.delay)

            if not alive and not can_wake:
                logger.info(f'Magic packet on cooldown {host.name=}')
                continue

            if not alive and can_wake:
                last_wake = now
                wakeonlan.send_magic_packet(host.mac)
                logger.info(f'Magic packet sent {host.name=}')
                continue

            logger.info(f'Host is alive {host.name=}')

    except asyncio.CancelledError:
        logger.info(f'Host monitor stopped {host.name=}')
