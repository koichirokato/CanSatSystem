import SocketCommunication
import json
import datetime
import time

socket = SocketCommunication.SocketCommunication("localhost", 8000)

socket.socket_client_up()

for i in range(5):
    recv_data = ''
    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    send_data_dict = {"time":now,"x":30,"y":30,"cansat id":2}
    send_data_json = json.dumps(send_data_dict)

    recv_data = socket.socket_com_client(send_data_json)

    # recv_data = socket.socket_recv()
    if(len(recv_data)!=0): print(recv_data)
    
    # socket.socket_send(send_data_json)
    print(i)
    # recv_data = socket.socket_com_client(send_data_json)

    # if(len(recv_data)!=0): recv_data_dict = json.loads(recv_data)

    # print("#####################")
    # for ele in recv_data_dict:
    #     print(str(ele) + ":" + str(recv_data_dict[ele]))
    # print("#####################")

    time.sleep(7)

# print("#####################")
# for ele in recv_data_dict:
#     print(str(ele) + ":" + str(recv_data_dict[ele]))
# print("#####################")