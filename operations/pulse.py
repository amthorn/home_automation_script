import asyncio

class Pulse:
    def __init__(self, after=600):
        self._after = after

    def __call__(self, device):
        if device:
            print(f"{device.alias}: On for {device.sys_info['on_time']}")
        if device.is_dimmable and device.is_on and device.sys_info['on_time'] > self._after:
            print(f"{device.alias}: Pulsing")
            return lambda: self._do(device)
        else:
            print(f"{device.alias}: Not pulsing")
            return lambda: asyncio.sleep(0)
    
    async def _do(self, device, count=5, state=1):
        # Dim from 100 to 0 in 0.5 seconds
        if state:
            # if on, dim to 0 to setup for pulsing
            [await device.set_brightness(i) for i in range(100, 1, -1)]
            
        for _ in range(count):
            [await device.set_brightness(i) for i in range(1, 101)]
            [await device.set_brightness(i) for i in range(100, 1, -1)]

        if state:
            # if on, turn back up after pulsing
            [await device.set_brightness(i) for i in range(1, 101)]