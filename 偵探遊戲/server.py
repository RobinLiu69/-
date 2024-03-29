import socket, json, re
import threading
from pwn import log

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

class Server:
    def __init__(self, cards: list[list[str, int]]=[], datas: dict[Datas]={}) -> None:
        log.success("Server initialized")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ("0.0.0.0", 40000)
        # self.server_address = (socket.gethostbyname(socket.gethostname()), 40000)
        # self.server_address = ("25.61.96.35", 32768)
        log.success(f"Server address(IPv4):{self.server_address}")
        self.server_socket.bind(self.server_address)
        self.server_socket.listen(8)
        log.success('Waiting clients to connect...')
        self.clients: list[socket.socket] = []
        self.cards: list[list[str, int]] = cards
        self.datas: dict[Datas, str] = datas
        self.find_client()
        
    def handle_client(self, client_socket: socket.socket) -> None:
        try:
            while True:
                data: bytes | bytearray = client_socket.recv(4096)
                if not data:
                    break
                raw = data.decode('utf-8')
                dataRes: str = re.findall("J->:.+?:<-J", raw)
                cardRes: str = re.findall("C->:.+?:<-C", raw)
                if dataRes or cardRes:
                    for data in dataRes:
                        try:
                            jsonData: str = json.loads(data[4:-4:].replace("'", "\""))
                            res: Datas = self.datas.get(jsonData["room_name"], None)
                            if not res:
                                self.datas[jsonData["room_name"]] = Datas(jsonData["room_name"], jsonData["items"], jsonData["players"])
                            else:
                                res.update(jsonData)
                        except:
                            print("Error decoding", data)
                    for data in cardRes:
                        try:
                            jsonData: str = json.loads(data[4:-4:].replace("'", "\""))
                            self.cards: Datas = jsonData
                        except:
                            print("Error decoding", data)
                else:
                    self.broadcast(data)
        except:
            pass

        client_socket.close()

    def broadcast(self, message: str) -> None:
        # print(clients)
        for client in self.clients[::-1]:
            # print(client)
            try:
                client.sendall(message)
            except Exception as e:
                # print(e)
                self.clients.remove(client)
                
    def send_data(self, client_socket: socket.socket, data:Datas = None, cards: list[str]=None) -> bool:
        try:
            if data != None:
                data = {"room_name" : data.name, "items" : data.items, "players" : data.players}
                client_socket.send(f"J->:{data}:<-J".encode('utf-8'))
            if cards != None:
                client_socket.send(f"C->:{cards}:<-C".encode('utf-8'))

            return True
        except Exception as e:
            print(e)
            print("Server are closed.")
            return False
        
    def find_client(self) -> None:
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                self.clients.append(client_socket)
                log.success(f"Connect from:{client_address}")
                for data in self.datas.items():
                    self.send_data(client_socket, data=data[1])
                self.send_data(client_socket, cards=self.cards)
                client_thread = threading.Thread(target=self.handle_client, args=[client_socket])
                client_thread.start()
                
        except KeyboardInterrupt:
            log.success("Server shut down")
            self.server_socket.close()
            
        except Exception as e:
            print(e)
            
        finally:
            for client in self.clients:
                client.close()
            self.server_socket.close()

if __name__ == "__main__":
    server = Server(cards=[["Take", 1], ["Kill", 2]], datas={"kitchen": Datas("kitchen", ["Take", "Kill", "Take"], ["robin"])})
    server.server_socket.close()