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

class Server:
    def __init__(self, cards: list[str]=[], datas: dict[Datas]={}) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('25.61.96.35', 12345)
        self.server_socket.bind(self.server_address)
        self.server_socket.listen(8)
        print('wauiting clients to connect...')
        self.clients: list[socket.socket] = []
        self.cards: list[str] = cards
        self.datas: dict = datas
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
                            data: str = json.loads(data[4:-4:].replace("'", "\""))
                            res: Datas = self.datas.get(data["room_name"], None)
                            if not res:
                                self.datas[data["room_name"]] = Datas(data["room_name"], data["items"], data["players"])
                            else:
                                res.update(data)
                        except:
                            print("Error decoding", data)
                    for data in cardRes:
                        try:
                            data: str = json.loads(data[4:-4:].replace("'", "\""))
                            self.cards: Datas = data
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
                
    def find_client(self) -> None:
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                self.clients.append(client_socket)
                print(f"connect from:{client_address}")

                client_thread = threading.Thread(target=self.handle_client, args=(client_socket))
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\nserver shut down")
        finally:
            for client in self.clients:
                client.close()
            self.server_socket.close()
            
if __name__ == "__main__":
    server = Server()
    server.server_socket.close()