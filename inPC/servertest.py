import SocketCommunication
import json
import datetime
import time

socket = SocketCommunication.SocketCommunication("localhost", 8000)

socket.socket_server_up()

now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

send_data_dict = {"time":now,"x":10,"y":10,"cansat id":1}
send_data_json = json.dumps(send_data_dict)

while True:
    recv_data = ''
    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    send_data_dict = {"time":now,"x":10,"y":10,"cansat id":1}
    send_data_json = json.dumps(send_data_dict)

    # socket.socket_send(send_data_json)
    recv_data = socket.socket_com_server(send_data_json)
    # recv_data = socket.socket_recv()
    if(len(recv_data)!=0): print(recv_data)
    time.sleep(5)

# recv_data = socket.socket_com_server(send_data_json)

# recv_data_dict = json.loads(recv_data)

# print("#####################")
# for ele in recv_data_dict:
#     print(str(ele) +":"+ str(recv_data_dict[ele]))
# print("#####################")