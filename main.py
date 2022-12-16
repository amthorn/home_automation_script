import asyncio
import time
from devices.fans import Fans
from devices.lights import Lights
from operations.timeout import Timeout
from operations.pulse import Pulse

rules = {
    'lights': {
        'Entryway Light': [
            Timeout(600),  # 10 minutes
        ],
        # 'Master Bedroom Light': [
        #     Pulse(10),
        # ]
    }
}

async def main_event_loop():
    while True:
        print("Discovering...")
        devices = {
            'lights': await Lights.create(),
            'fans': await Fans.create()
        }
        print("Applying rules...")
        try:
            for category, targets in rules.items():
                for name, operations in targets.items():
                    # get the device
                    device = devices[category]._devices.get(name)
                    for operation in operations:
                        await operation(device)()
        except Exception as e:
            print(f"{str(type(e))}: {e}")


if __name__ == "__main__":
    asyncio.run(main_event_loop())