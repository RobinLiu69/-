import socket, json, re
import threading, time
from pwn import log

class Items:
    def __init__(self, name: str, history: list[str]=[], covered: int=0) -> None:
        self.name: str = name
        self.history: list[str] = history
        self.covered: int = covered
class Datas:
    def __init__(self, name: str, items: list[dict]=[], players: list[str]=[]) -> None:
        self.name: str = name
        self.items: list[Items] = list(Items(item["name"], item["history"], item["covered"]) for item in items)
        self.players: list[str] = players
        
    def update(self, kwargs: dict) -> None:
        for key, value in kwargs.items():
            if key == "items":
                self.items: list[Items] = list(Items(item["name"], item["history"], int(item["covered"])) for item in value)
            elif key == "players":
                self.players = value

class Client:
    def __init__(self, server_address: str) -> None:
        log.success("Client initialized")
        self.server_close = False
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (server_address, 40000)
        self.datas: dict[Datas] = {}
        self.cards: list[str] = []
        
        while not self.connect(): log.success("Retrying to connect...")

    def connect(self) -> bool:
        time.sleep(1)
        log.success("Trying to connect to server...")
        try:
            time.sleep(1.5)
            self.client_socket.connect(self.server_address)
            self.receive_thread = threading.Thread(target=self.receive_data, args=[self.client_socket])
            self.receive_thread.start()
            log.success("Connected")
            return True
        except KeyboardInterrupt:
            log.success("\nStop the process")
            return True
        except Exception as e:
            print(e)
            time.sleep(3)
        except:
            log.error("Server has not activated, please wait...")
            # self.server_close = True
            return False
        
    def receive_data(self, client_socket: socket.socket) -> None:
        # try:
            while True:
                data:  bytes | bytearray  = client_socket.recv(2048)
                if not data:
                    break
                data = data.decode('utf-8')
                dataRes = re.findall("J->:.+?:<-J", data)
                print(dataRes)
                cardRes = re.findall("C->:.+?:<-C", data)
                if dataRes or cardRes:
                    for data in dataRes:
                        # try:
                            jsonData = json.loads(data[4:-4:].replace("'", "\""))
                            self.datas[jsonData["room_name"]] = Datas(jsonData["room_name"], jsonData["items"], jsonData["players"])
                            print("Received JSON data:", jsonData)
                        # except Exception as e:
                        #     print("Error decoding", data, e)

                    for data in cardRes:
                        try:
                            jsonData: str = json.loads(data[4:-4:].replace("'", "\""))
                            self.cards: list[str] = jsonData
                        except Exception as e:
                            print("Error decoding", data, e)
                        
        # except Exception as e:
        #     print(e)
        #     if str(e) != "[WinError 10053] 連線已被您主機上的軟體中止。":
        #         log.success("Server isn't started, relunch the server to connet to it.")
            

        #    client_socket.close()
        
    def send_data(self, room_name: str=None, items: list[Items]=None, players: list[str]=None, cards: list[str]=None) -> bool:
        try:
            if room_name != None:
                data = {"room_name" : room_name, "items" : items, "players" : players}
                print("sent:", data)
                self.client_socket.send(f"J->:{data}:<-J".translate(str.maketrans("()", "[]")).encode('utf-8'))
            elif cards != None:
                self.client_socket.send(f"C->:{cards}:<-C".encode('utf-8'))
            else:
                return False
            return True
        except Exception as e:
            print(e)
            log.success("Server are closed.")
            return False

    
    
def main() -> int:
    robin = Client("25.42.132.180")



    return 0    
        
if __name__ == "__main__":
    main()