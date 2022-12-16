import asyncio

class Timeout:
    def __init__(self, timeout=600):
        self._timeout = timeout

    def __call__(self, device):
        print(f"{device.alias}: On for {device.sys_info['on_time']}")
        if device.is_on and device.sys_info['on_time'] > self._timeout:
            print(f"{device.alias}: Turning Off")
            return device.turn_off
        else:
            print(f"{device.alias}: Not turning off")
            return lambda: asyncio.sleep(0)