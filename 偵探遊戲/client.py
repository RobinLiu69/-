import socket, json, re
import threading, time

class Datas:
    def __init__(self, name: str, items: list[str]=[], players: list[str]=[]) -> None:
        self.name: str = name
        self.items: list[str] = items
        self.players: list[str] = players
        
    def update(self, kwargs: dict) -> None:
        for key, value in kwargs.items():
            if key == "items":
                self.items = value
            elif key == "players":
                self.players = value

class Client:
    def __init__(self, server_address: str) -> None:
        self.server_close = False
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (server_address, 12345)
        self.datas: dict[Datas] = {"kitchen":Datas("kitchen", ["notebook", "food"], ["robin"])}
        self.cards: list[str] = []
        
        while not self.connect(): print("Retrying to connect...")

    def connect(self) -> bool:
        print("Trying to connect to server...")
        try:
            time.sleep(1.5)
            self.client_socket.connect(self.server_address)
            self.receive_thread = threading.Thread(target=self.receive_data, args=[self.client_socket])
            self.receive_thread.start()
            print("Connected")
            return True
        except KeyboardInterrupt:
            print("\nStop the process")
            return True
        except:
            print("Server has not activated, please wait...")
            # self.server_close = True
            return False
        
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
                            jsonData: str = json.loads(data[4:-4:].replace("'", "\""))
                            self.cards: Datas = jsonData
                        except:
                            print("Error decoding", data)
                        
        except Exception as e:
            print(e)
            if str(e) != "[WinError 10053] 連線已被您主機上的軟體中止。":
                print("Server isn't started, relunch the server to connet to it.")
            

        client_socket.close()
        
    def send_data(self, room_name: str, items: list[str], players: list[str], cards: list[str]) -> bool:
        try:
            data = {"room_name" : room_name, "items" : items, "players" : players}
            
            self.client_socket.send(f"J->:{data}:<-J".encode('utf-8'))
            self.client_socket.send(f"C->:{cards}:<-C".encode('utf-8'))
            return True
        except Exception as e:
            print(e)
            print("Server are closed.")
            return False
        
    
    
def main() -> int:
    robin = Client("192.168.232.233")
    
    
    
    return 0    
        
if __name__ == "__main__":
    main()