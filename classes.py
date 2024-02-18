class WakeConfig:
    def __init__(self, charge: int, runtime: int, status: str):
        self.charge = charge
        self.runtime = runtime
        self.status = status


class UPSStatus:
    def __init__(self, charge: int, runtime: int, status: str):
        self.charge = charge
        self.runtime = runtime
        self.status = status


class Host:
    def __init__(self, name: str, mac: str, address: str):
        self.name = name
        self.mac = mac
        self.address = address
