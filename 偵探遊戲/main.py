import pygame
import client, server
import cards as c
import room as r
from os import path


class Screen:
    def __init__(self, width: int=None, height: int=None) -> None:
        self.width, self.height = width, height
        self.width, self.height = self.info()
        if self.width/self.height != 1.6:
            self.resize()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("nunu")
    
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
        self.screen.fill((255, 255, 255))
    
    def flip(self) -> None:
        pygame.display.flip()

def init():
    pygame.init()
    Online = client.Client(input())
    screen = Screen()
    # Online = client.Client("13.76.138.194")
    rooms: list[r.Room] = []
    return Online, rooms, screen


def room_selection(screen: Screen, rooms: list[r.Room]) -> r.Room:
    nearst: r.Room = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if nearst != None:
                    running = False
        screen.fill()
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for room in rooms:
            if nearst == None:
                nearst = room
            if nearst.distance(mouse_x, mouse_y) > room.distance(mouse_x, mouse_y):
                nearst = room
        
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
        
        room.update(screen, Online.datas[room.name])
       
       
        screen.flip()
    return  None
    
def main() -> int:
    
    Online, rooms, screen = init()
    
    # roomlist.append(Room("kitchen"), Room("bedroom"), Room("yard"),Room("study"), Room("liviingroom"))
    room_map = r.Map(screen.info(), (screen.width/1.5, screen.height/1.5))
    rooms.append(r.Room("kitchen", screen.info()))
    for room in rooms:
        room.data_update(Online.datas[room.name])
        print(room.info())
    
    
    
    for i in range(5):
        Online.send_data(cards=c.draw_card(Online.cards))
    
    print("selecting rooms...")
    the_room = room_selection(screen, rooms)
    
    print("entering the room...")
    enter_room(Online, screen, the_room)



if __name__ == "__main__":
    main()