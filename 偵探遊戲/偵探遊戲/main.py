import pygame
import connect, threading
from setting import *

class Player:
    def __init__(self) -> None:
        self.name = input("輸入用戶名")
        self.job = ""
        self.handcard = ["take", "take", "put down"]



class Rooms:
    def __init__(self, name, rooms:list["Rooms"]) -> None:
        self.name = name
        self.items = ["gun", "food"]
        self.players: list[Player] = []
        self.furniture = []
        rooms.append(self)
    
        
    def enter(self, player: Player) -> int:
        self.players.append(player.name)
    
    def leave(self, player: Player) -> int:
        self.players.remove(player.name)
    
    def select(self) -> int:
        choise = input("輸入拿取第幾項:")
        if choise.isdigit():
            return int(choise)-1
        else:
            if choise.lower() == "exit": 
                print("exit")
                return -1
            else:
                print("無效動作")
                return -1
            
    def pack(self) -> tuple:
        return [self.name, self.items, self.players, self.furniture]
        
    
    def take(self, player: Player) -> int:
        print(f"{self.name}-items: "+" ".join(f"{index+1}:{value}" for index, value in enumerate(self.items)))
        select = self.select()
        if select > -1:
            if self.items[select] in card:
                return 1
            player.handcard.append(self.items.pop(select))
            self.items.append("taken")
            return 0
        else:
            return 1
    
    def put_down(self, player: Player) -> int:
        print(f"{player.name}-handcard: "+" ".join(f"{index+1}:{value}" for index, value in enumerate(player.handcard)))
        select = self.select()
        if select > -1:
            if player.handcard[select] in card:
                return 1
            self.items.append(player.handcard.pop(select))
            self.items.append("put down")
            return 0
        else:
            return 1
        
    def swap(self, player:Player) -> int:
        print(f"{self.name}-items"+" ".join(f"{index+1}:{value}" for index, value in enumerate(self.items)))
        select = self.select()
        if select > -1:
            temp = player.handcard.pop(select)
            print(f"{self.name}-items: "+" ".join(f"{index+1}:{value}" for index, value in enumerate(self.items)))
            select = self.select()
            self.items.insert(select, temp)
            self.items.append("swapped")
            return 0
        else:
            return 1
        
        
    def interact(self, action : str, player: Player, online: connect.Online) -> int:
        if action == "take" and "take" in player.handcard:
            self.take(player)
        elif action == "put_down" and "put down" in player.handcard:
            self.put_down(player)
        elif action == "swap" and "swap" in player.handcard:
            self.swap(player)
        elif action.lower() == "d":
            print(self.pack(), "\n", online.data)
        elif action.lower() == "exit":
            self.leave(player)
            return 0
        
        online.update(player.name, self.pack())
        return 1
    
def go_to_room(rooms: list[Rooms], player: Player, online: connect.Online) -> int:
    print(" ".join(room.name for room in rooms))
    select = input("輸入房間名子:")
    Troom = None
    for index, room in enumerate(rooms):
        if room.name == select:
            Troom = room
            break
        
    if Troom != None:
        Troom.enter(player)
        running = True
        while running:
            threading.Thread(target=update_room, args=(rooms, online)).start()
            print(f"{player.name}-handcard"+" ".join(f"{index+1}:{value}" for index, value in enumerate(player.handcard)))
            running = Troom.interact(input("輸入 take 拿取 put_down 放下 swap 置換 exit 退出"), player, online)
        
        
    print("結束回合")
               
def update_room(rooms: list[Rooms], online: connect.Online):
    try:
        for index, room in enumerate(rooms):
            print(room, online.data)
            if room.name == online.data[1][0]:
                room.items = online.data[1][1]
                room.players = online.data[1][2]
                room.furniture = online.data[1][3]
                print('update')
    except:
        ...

def main() -> int:
    card = ["taken", "put down", "swapped"]
    rooms: list[Rooms] = []
    Rooms("kitchen", rooms)
    
    player = Player()
    online = connect.Online()
    running = True
    
    try:
        while running:

            go_to_room(rooms, player, online)
            if input("退出?(y/n):").lower() == "y":
                online.shut_down()
                running = False
            
    except KeyboardInterrupt:
        online.shut_down()
            
    return 0    
    
    
    
if __name__ == "__main__":
    main()
    # ttt\
        