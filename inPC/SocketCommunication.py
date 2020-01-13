import socket

class SocketCommunication:
    def __init__(self):
        self.s          = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Ip_address = 1
        self.Port = 8000
    
    def socket_server_up(self):
        self.s.bind(("localhost", 50007))    # 指定したホスト(IP)とポートをソケットに設定
        self.s.listen(1)                     # 1つの接続要求を待つ
        self.s, addr = self.s.accept()       # 要求が来るまでブロック
        print("Conneted by"+str(addr))  #サーバ側の合図

    def socket_client_up(self):
        self.s.connect(("localhost", 50007))

    def socket_com_client(self, data):
        recv_data = self.s.recv(1024)
        recv_data = recv_data.decode()
        print("Server>", recv_data)        # サーバー側の書き込みを表示
        # send_data = input("Client>")     # 入力待機
        send_data = data
        self.s.send(send_data.encode())  # ソケットに入力したデータを送信

        if send_data == "q":               # qが押されたら終了
            self.s.close()

    def socket_com_server(self, data):
        # send_data = input("Server>")     # 入力待機(サーバー側)
        send_data = data
        self.s.send(send_data.encode())    # ソケットにデータを送信
        recv_data = self.s.recv(1024)      # データを受信（1024バイトまで）
        recv_data = recv_data.decode()
        print("Client>",recv_data)         # サーバー側の書き込みを表示
        if recv_data == "q":               # qが押されたら終了
            self.s.close()