import socket, json, re, threading

"""
This class is used to connect to the server and update the data
"""
class Online:
    def __init__(self):
        self.name = socket.gethostname()
        self.ip = socket.gethostbyname(self.name)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.other_server_address = []
        self.port = 10101
        self.data = 0
        print(f"Self IP:{self.ip}, Self Port:{self.port}")
        self.other_server_address = input("input others ip(ipv4)")
        self.find_player()

    def find_player(self):
        client_socket, client_address = self.start_server()
        self.receive_thread = threading.Thread(target=self.receive_message, args=(client_socket,client_address))
        self.receive_thread.start()

    def update(self, name, data):
        """
        Update the data
        Args:
            name (str): The name of the user
            data (str): The data to be updated
        """
        encodeData = self.pack_data(name, data)
        self.send_message(encodeData)

    def receive_message(self, client_socket: socket.socket, client_address: int):
        """
        Receive the message from the server
        Args:
            client_socket (socket.socket): The socket of the client
            client_address (int): The address of the client
        """
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
            pass

    def shut_down(self):
        """
        Shut down the server and the client
        """
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

    def pack_data(self, name: str, data: str):
        """
        Pack the data into a json format
        Args:
            name (str): The name of the user
            data (str): The data to be sent
        Returns:
            str: The packed data
        """
        if "exit" in data:
            self.shut_down()
        data = {"playername": name, "data": data}
        return f"J->:{data}:<-J".encode('utf-8')

    def send_message(self, message: str):
        """
        Send the message to the server
        Args:
            message (str): The message to be sent
        Returns:
            bool: Whether the message is sent successfully or not
        """
        try:
            if message:
                self.client_socket.sendall(message)
                return True
            return False
        except Exception as e:
            print(f"{e}")
            return False

    def start_server(self):
        """
        Start the server
        Returns:
            tuple: The client socket and the client address
        """
        try:
            self.server_socket.bind((self.ip, self.port))
        except OSError as e:
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
    
    
    