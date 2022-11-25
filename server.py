import socket
from struct import unpack
import json


ids_to_name: dict = {
    1: "canCoder right front",
    2: "canCoder right rear",
    3: "canCoder left rear",
    4: "canCoder left front",

    11: "driveMotor right front",
    12: "driveMotor right rear",
    13: "driveMotor left rear",
    14: "driveMotor left front",

    21: "rotationMotor right front",
    22: "rotationMotor right rear",
    23: "rotationMotor left rear",
    24: "rotationMotor left front"
}

log_data_to_save = json.load(open("./data.json", "r"))

for value in ids_to_name:
    log_data_to_save[value] = []

with open("./data.json", "w") as json_file:
    json.dump(log_data_to_save, json_file)

HOST: str = socket.gethostbyname(socket.gethostname())
print(HOST)

PORT = 2230

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
    socket_server.bind((HOST, PORT))
    socket_server.listen()

    connection, address = socket_server.accept()
    print("connection accepted")

    with connection:
        while True:
            try:
                input_id: int = int(unpack(">i", connection.recv(4))[0]) # java sends big first -> that's why big emdian
                value: float = float(unpack(">d", connection.recv(8))[0]) # java sends big first -> that's why big emdian
                
                print(input_id, round(value, 3))

                log_data_to_save[ids_to_name[input_id]].append(value)
                with open("./data.json", "w") as json_file:
                    json.dump(log_data_to_save, json_file)

            except Exception as e:
                socket_server.close()
                break