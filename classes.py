class WakeConfig:
    def __init__(
            self,
            batt_level_gte: int,
            runtime_gte: int,
            ups_status_str: str,
    ):
        self.batt_level_gte = batt_level_gte
        self.runtime_gte = runtime_gte
        self.ups_status_str = ups_status_str


class UPSStatus:
    def __init__(
            self,
            battery_charge: int,
            battery_runtime: int,
            ups_status_str: str,
    ):
        self.battery_charge = battery_charge
        self.battery_runtime = battery_runtime
        self.ups_status_str = ups_status_str


class Host:
    def __init__(
            self,
            name: str,
            mac: str,
            address: str,
    ):
        self.name = name
        self.mac = mac
        self.address = address
