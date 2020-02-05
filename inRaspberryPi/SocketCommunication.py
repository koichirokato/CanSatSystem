#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import time

class SocketCommunication:
    def __init__(self, ip_address, port):
        # self.s          = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip_address = ip_address
        self.Port       = port
    
    def socket_server_up(self):
        print("wainting...")
        self.s          = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.ip_address, self.Port))    # 指定したホスト(IP)とポートをソケットに設定
        self.s.listen(1)                     # 1つの接続要求を待つ
        self.s, addr = self.s.accept()       # 要求が来るまでブロック
        print("Conneted by"+str(addr))       #サーバ側の合図

    def socket_client_up(self):
        self.s          = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("ip_address : " + str(self.ip_address) + ", Port : " + str(self.Port))
        while True:
            try:
                self.s.connect((self.ip_address, self.Port))
                print("connection success")
                break
            except ConnectionRefusedError:
                # 接続先のソケットサーバが立ち上がっていない場合、
                # 接続拒否になることが多い
                print('Refused Error')
                print('retry in 5seconds')
                for i in range(5):
                    print(str(5-i) + "...")
                    time.sleep(1)

    def socket_com_client(self, data):
        try:
            recv_data = self.s.recv(1024)
            if(len(recv_data)!=0):
                recv_data = recv_data.decode()
        except socket.error:
            print("connection lost")
            self.s.close()
            SocketCommunication.socket_client_up(self)
    
        send_data = data
        try:
            self.s.send(send_data.encode())
        except socket.error:
            print("connection lost, try reconnect")
            self.s.close()
            SocketCommunication.socket_client_up(self)
        return recv_data

    def socket_com_server(self, data):
        send_data = data
        self.s.send(send_data.encode())
        try:
            recv_data = self.s.recv(1024)
            recv_data = recv_data.decode()
            return recv_data
        except socket.error:
            print("connection lost")
            self.s.close()
            SocketCommunication.socket_server_up(self)

    def socket_recv(self):
        try:
            recv_data = self.s.recv(1024)
            return recv_data
        except socket.error:
            print("connection lost")
            self.s.close()
            SocketCommunication.socket_server_up(self)

    def socket_send(self, data):
        send_data = data
        self.s.send(send_data.encode())