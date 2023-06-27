from app import db, app
from app.models import DistanceData
import socket
import time

bufferSize = 1024

serverAddress = ("192.168.0.91", 2222)

UDPClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while (True):
    cmd = "GO"
    cmd = cmd.encode("utf-8")
    UDPClient.sendto(cmd, serverAddress)
    data, address = UDPClient.recvfrom(bufferSize)

    data = data.decode("utf-8")
    
    with app.app_context():
        db.create_all()
        distance = DistanceData(distance = data)
        db.session.add(distance)
        db.session.commit()

    print("Distance: ", data, "inches")

    time.sleep(1)