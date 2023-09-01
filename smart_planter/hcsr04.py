import socket
import time

from planter import app
from planter.models import WaterLevelData, db

bufferSize = 1024

# we may consider getting the IP and PORT from environment variables if they vary
# in the future we will implement reading from .env using python_dotnev module
serverAddress = ("192.168.0.90", 2222)

UDPClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    cmd = "GO"
    cmd = cmd.encode("utf-8")
    UDPClient.sendto(cmd, serverAddress)
    data, address = UDPClient.recvfrom(bufferSize)

    data = data.decode("utf-8")

    with app.app_context():
        db.create_all()
        distance = WaterLevelData(distance=data)
        db.session.add(distance)
        db.session.commit()

    print("Distance: ", data, "inches")

    time.sleep(1)
