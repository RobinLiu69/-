import pygame
import client, server, threading
import cards as c
from os import path
import types



class Room:
    def __init__(self, room_name: str, size: tuple[int, int]) -> None:
        self.name = room_name
        self.x = 0
        self.y = 0
        self.items = []
        self.players = []
        self.width = size[0]
        self.height = size[1]
        self.imageOriginal = pygame.Surface((self.width, self.height))
        self.imageOriginal.fill((255,255,255))
        self.imageOriginal.blit(source = pygame.transform.scale(pygame.image.load(path.join("image/"+room_name+".png")).convert_alpha(),(180, 180)), dest = (0,0))
        self.imageOriginal.set_colorkey((255,255,255))
        self.image = self.imageOriginal.copy()

    def distance(self, x: int, y: int) -> float:
        dx = x - self.x
        dy = y - self.y
        return (dx**2+dy**2)**0.5
    
    def update(self, surface: pygame.surface.Surface, data: client.Datas) -> None:
        self.draw(surface)
        self.data_update(data)
    
    def change(self, online: client.Client):
        online.send_data(self.name, self.items, self.players)
    
    def data_update(self, data: client.Datas) -> int:
        try:
            self.items = data.items
            self.players = data.players
            print("data update")
            return 0
        except Exception as e:
            print(e)
            return 1
    
    def info(self) -> tuple[str, list[str], list[str]]:
        return self.name, self.items, self.players
        
    def draw(self, surface: pygame.surface.Surface) -> int:
        try:
            surface.blit(self.image, (self.x,self.y))
            return 0
        except Exception as e:
            print(e)
            return 1

class Screen:
    def __init__(self, width: int=None, height: int=None) -> None:
        self.width, self.height = width, height
        self.width, self.height = self.info()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("nunu")
        
    def info(self) -> tuple[int, int]:
        try:
            return self.width/1, self.height/1
        except:
            return pygame.display.get_desktop_sizes().pop()
        
        
    def fill(self) -> None:
        self.screen.fill((255, 255, 255))
    
    def flip(self) -> None:
        pygame.display.flip()


def room_selection(screen: Screen, rooms: list[Room]) -> int:
    nearst: Room = None
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
    return 0

def init():
    pygame.init()
    screen = Screen()
    Online = client.Client(input())
    # Online = client.Client("13.76.138.194")
    rooms: list[Room] = []
    return Online, rooms, screen
    
    
def main() -> int:
    
    Online, rooms, screen = init()
    
    # roomlist.append(Room("kitchen"), Room("bedroom"), Room("yard"),Room("study"), Room("liviingroom"))
    rooms.append(Room("kitchen", screen.info()))
    for room in rooms:
        room.data_update(Online.datas[room.name])
        print(room.info())
    running = True
    font = pygame.font.Font(None, 36)
    Online.send_data(cards=c.draw_card(Online.cards))
    
    room_selection(screen, rooms)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill()
        
        screen.flip()
    return 0



if __name__ == "__main__":
    main()
