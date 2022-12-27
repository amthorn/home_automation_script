import asyncio
import http.server
import os
import socketserver
from teslajsonpy import Controller
from http import HTTPStatus

async def preheat_async(client, temperature, vin):
    await client.connect()
    await client.generate_car_objects(wake_if_asleep=True)
    await client.cars[vin].set_temperature(temperature)
    await client.cars[vin].set_hvac_mode(value='on')
    await client.cars[vin].set_heated_steering_wheel(value='on')
    # level: 0 (off), 1 (low), 2 (medium), 3 (high)
    # seat_id: 
    # 0 (front left)
    # 1 (front right)
    # 2 (rear left)
    # 4 (rear center)
    # 5 (rear right)
    # 6 (third row left)
    # 7 (third row right)
    await client.cars[vin].remote_seat_heater_request(seat_id=0, level=2)


def preheat():
    client = Controller(
        email='avatheavian@gmail.com',
        access_token=os.environ['TESLA_ACCESS_TOKEN'],
        refresh_token=os.environ['TESLA_REFRESH_TOKEN']
    )
    asyncio.run(preheat_async(client, float(os.environ['TESLA_TARGET_TEMP_C']), os.environ['TESLA_VIN']))


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        preheat()


httpd = socketserver.TCPServer(('', 8000), Handler)
httpd.serve_forever()


if __name__ == "__main__":
    preheat()
