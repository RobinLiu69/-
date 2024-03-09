import socket, json, re
import threading

class Datas:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.items: list[str] = []
        self.players: list[str] = []
        
    def update(self, kwargs: dict) -> None:
        for key, value in kwargs.items():
            if key == "items":
                self.items = value
            elif key == "players":
                self.players = value

class Message():
    def __init__(self) -> None:
        self.server_close = False
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('25.36.126.26', 12345)
        try: 
            self.client_socket.connect(self.server_address)
            self.receive_thread = threading.Thread(target=self.receive_data, args=(self.client_socket))
            self.receive_thread.start()
        except: 
            self.error_message = "Server has not activated, please wait."
            self.server_close = True

        self.datas = {}
    def receive_data(self, client_socket: socket.socket) -> None:
        try:
            while True:
                data:  bytes | bytearray  = client_socket.recv(1024)
                if not data:
                    break
                data = data.decode('utf-8')
                
                dataRes = re.findall("J->:.+?:<-J", data)
                cardRes = re.findall("C->:.+?:<-C", data)
                if dataRes or cardRes:
                    for data in dataRes:
                        try:
                            jsonData = json.loads(data[4:-4:].replace("'", "\""))
                            self.datas[jsonData["room_name"]] = Datas((jsonData["room_name"], jsonData["items"]), jsonData["players"])
                        except:
                            print("Error decoding", data)
                    for data in cardRes:
                        try:
                            jsonData = json.loads(data[4:-4:].replace("'", "\""))
                            self.datas[jsonData["room_name"]] = Datas((jsonData["room_name"], jsonData["items"]), jsonData["players"])
                        except:
                            print("Error decoding", data)
                        
        except Exception as e:
            print(str(e))
            # ConnectionAbortedError.winerror.
            if str(e) != "[WinError 10053] 連線已被您主機上的軟體中止。":
                print("伺服器未開啟，資料傳輸與接收已關閉，重啟遊戲可重新連接")
            pass

        client_socket.close()
        
    def send_data(self, user_name, pos, rotate):
        try:
            data = {"user_name" : user_name, "x" : pos[0], "y" : pos[1], "rotate" : rotate}
            # encoded_data = json.dumps(data).encode()
            self.client_socket.send(f"J->:{data}:<-J".encode('utf-8'))
        except Exception as e:
            print(e)
            print(1)
            print("客户端关闭")