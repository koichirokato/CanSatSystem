import SocketCommunication
import json
import datetime
import time

socket = SocketCommunication.SocketCommunication("localhost", 8000)

socket.socket_client_up()


for i in range(5):

    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    send_data_dict = {"time":now,"x":30,"y":30,"cansat id":2}
    send_data_json = json.dumps(send_data_dict)

    recv_data = socket.socket_com_client(send_data_json)

    recv_data_dict = json.loads(recv_data)



    print("#####################")
    for ele in recv_data_dict:
        print(str(ele) + ":" + str(recv_data_dict[ele]))
    print("#####################")

    time.sleep(5)

print("#####################")
for ele in recv_data_dict:
    print(str(ele) + ":" + str(recv_data_dict[ele]))
print("#####################")