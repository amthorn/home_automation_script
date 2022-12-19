
import kasa

class Kasa:
    async def _discover_devices(self, callback):
        await kasa.Discover.discover(on_discovered=callback)

    @classmethod
    async def create(cls):
        self = cls()
        for i in range(5):
            await self._discover()
            if self._devices:
                break
            print(f"Discovery Failed: {i}/5")
        return self

    async def _discover(self):
        self._devices = {}
        await self._discover_devices(callback=self.setup)

    async def setup(self, device):
        if self.CATEGORY in device.alias:
            self._devices[device.alias] = device
