
import kasa

class Kasa:
    async def _discover_devices(self, callback):
        await kasa.Discover.discover(on_discovered=callback)

    @classmethod
    async def create(cls):
        self = cls()
        await self._discover()
        return self

    async def _discover(self):
        self._devices = {}
        await self._discover_devices(callback=self.setup)

    async def setup(self, device):
        if self.CATEGORY in device.alias:
            self._devices[device.alias] = device
