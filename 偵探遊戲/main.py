import pygame
import client, server
import cards as c
import room as r
from os import path


class Screen:
    def __init__(self, width: int=None, height: int=None) -> None:
        self.width, self.height = width, height
        self.width, self.height = self.info()
        print(self.width, self.height)
        if self.width/self.height != 1.6:
            self.resize()
        self.screen = pygame.display.set_mode((self.width, self.height))
        print(self.width, self.height)
        pygame.display.set_caption("Detective Game")
    
    def resize(self):
        for i in range(1000, self.width):
            for j in range(900, self.height):
                if i/j == 1.6:
                    self.width, self.height = i, j
    
    def info(self) -> tuple[int, int]:
        try:
            return self.width/1, self.height/1
        except:
            return pygame.display.get_desktop_sizes().pop()
        
        
    def fill(self) -> None:
        self.screen.fill((0, 0, 0))
    
    def flip(self) -> None:
        pygame.display.flip()

def init():
    pygame.init()
    Online = client.Client(input())
    screen = Screen()
    # Online = client.Client("13.76.138.194")
    rooms: list[r.Room] = []
    return Online, rooms, screen


def room_selection(screen: Screen, rooms: list[r.Room], room_map: r.Map) -> r.Room:
    nearst: r.Room = None
    running = True
    print(screen.width*2/5, screen.height/16*11.5)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("touch")
                if nearst != None:
                    running = False
        screen.fill()
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # print(mouse_x, mouse_y)
        nearst = room_map.detect(mouse_x, mouse_y, screen.info(), rooms, nearst)
        print(nearst)
        room_map.update(screen.screen)
        
        for room in rooms:
            room.drawC(screen.screen, screen.width)
        
        screen.flip()
    return nearst
    
def enter_room(Online: client.Client, screen: Screen, room: r.Room) -> None:
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                    ...
        screen.fill()
        
        room.update(screen.screen, Online.datas[room.name])
       
       
        screen.flip()
    return  None
    
def main() -> int:
    
    Online, rooms, screen = init()
    
    # roomlist.append(Room("kitchen"), Room("bedroom"), Room("yard"),Room("study"), Room("liviingroom"))
    rooms.append(r.Room("kitchen", screen.info(), screen.width*2/5, screen.height/16*11.5))
    
    room_map = r.Map(screen.info(), (screen.width, screen.height), rooms)
    for room in rooms:
        room.data_update(Online.datas[room.name])
        print(room.info())
    
    
    try:
        for i in range(5):
            Online.send_data(cards=c.draw_card(Online.cards))
    except:
        print("card list empty")
    
    
    print("selecting rooms...")
    the_room = room_selection(screen, rooms, room_map)
    
    print("entering the room...")
    if the_room != None:
        enter_room(Online, screen, the_room)



if __name__ == "__main__":
    main()