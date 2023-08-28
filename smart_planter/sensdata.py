#from planter import db, create_app
from planter import db, app
from planter.models import WeatherData, WaterLevelData
import socket, time

#app = create_app()
bufferSize = 1024

serverAddress = ("192.168.0.90", 2223) #(IP, PORT); IP may vary

UDPClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Client ready to recieve data . . .")

while (True):
    cmd = "GO"
    cmd = cmd.encode("utf-8")
    UDPClient.sendto(cmd, serverAddress)
    data, address = UDPClient.recvfrom(bufferSize)

    data = data.decode("utf-8")
    dataArray = data.split(":")
    
    with app.app_context():
        db.create_all()
        dataArray[0] = (float(dataArray[0]) * 1.8) + 32
        newSensData = WeatherData(temp = dataArray[0], humidity = dataArray[1])
        distance = WaterLevelData(distance = dataArray[2])
        db.session.add(newSensData)
        db.session.add(distance)
        db.session.commit()

    if (len(dataArray) == 1):
        print("No data")
    
    if (len(dataArray) == 3):
        print("Temperature: ", dataArray[0], "Humidity:", dataArray[1], "% Water Level: ", dataArray[2], "inches")

    time.sleep(1)