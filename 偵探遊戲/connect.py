import socket, json, re, threading

class Data():
    def __init__(self, userName: str,score: int, player1:list, player2:list, p1clock: int, p2clock: int, player1Hand: list, player2Hand: list, player1Decklen: int, player2Decklen: int,
        player1Trashlen: int, player2Trashlen: int, player1atk: int, player2atk: int, player1Token: int, player2Token: int, player1Luck: int, player2Luck: int, player1Tomtem: int, player2Tomtem: int):
        return True
        

class Online():
    def __init__(self):
        self.name = socket.gethostname()
        self.ip = socket.gethostbyname(self.name)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.other_server_address = []
        self.port = 10101
        self.data = 0
        self.clients: list[socket.socket] = []
        print(f"Self IP:{self.ip}, Self Port:{self.port}")
        self.other_server_address = input("input others ip(ipv4)")
        threading.Thread(target=self.find_player).start()
        
    def find_player(self):
        # while True:
        #     try:
        client_socket, client_address = self.start_server()
        if client_socket and client_address:
            self.clients.append(client_socket)
            self.receive_thread = threading.Thread(target=self.receive_message, args=(client_socket,client_address))
            self.receive_thread.start()
            # except KeyboardInterrupt:
            #     print("server close")
            # finally:
            #     for client in self.clients:
            #         client.close()
            #     self.server_socket.close()



    def update(self, name, data):
        encodeData = self.pack_data(name, data)
        self.send_message(encodeData)
        
    def receive_message(self, client_socket: socket.socket, client_address: int):
        try:
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                dataRes = re.findall("J->:.+?:<-J", data)
                for data in dataRes:
                    try:
                        jsonData = json.loads(data[4:-4:].replace("'", "\""))
                        self.data = [jsonData["playername"], jsonData["data"]]
                        print(self.data)
                    except Exception as e:
                        print(f"{e}")
                        print("Error decoding", data)
        except Exception as e:
            print(f"{e}")
         

        
    def shut_down(self):
        try:
            self.client_socket.close()
            print("client_socket closed")
        except:
            pass
        try:
            self.server_socket.close()
            print("server_socket closed")
        except:
            pass
        return False
        
    def pack_data(self, name, data):
        if "exit" in data:
            self.shut_down()
        data = {"playername": name, "data": data}
        return f"J->:{data}:<-J".encode('utf-8')
    
    
    
    
    def send_message(self, message):
        try:
            if message:
                self.client_socket.sendall(message)
                return True
            return False
        except Exception as e:
            print(f"{e}")
            return False

    
    def start_server(self):
        try:
            self.server_socket.bind((self.ip, self.port))
        except OSError as e:
            # print(f"OSError: {e}")
            return False, False
        self.server_socket.listen(10)
        print('Server is listening for connections...')
        
        try:
            self.client_socket.connect((self.other_server_address, self.port))
        except ConnectionRefusedError:
            print("ConnectionRefusedError")
            return False, False
        except socket.gaierror:
            print("socket.gaierror")
            return False, False
        print("Connected to server")
        client_socket, client_address = self.server_socket.accept()
        print(f'Connection from {client_address}')
        return client_socket, client_address
