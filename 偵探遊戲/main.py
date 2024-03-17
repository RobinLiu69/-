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
        
    def update(self, surface: pygame.surface.Surface, data: client.Datas) -> None:
        self.draw(surface)
        self.data_update(data)
    
    def change(self, online: client.Client):
        online.send_data(self.name, self.items, self.players)
    
    def data_update(self, data: client.Datas) -> int:
        try:
            self.items = data.items
            self.players = data.players
            print("data_update")
            return 0
        except Exception as e:
            print(e)
            return 1

        
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
        
        
    def update1(self) -> None:
        self.screen.fill((0, 0, 0))
    
    def update2(self) -> None:
        pygame.display.flip()
    
def room_selection(screen) -> int:
    while running == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
        
        screen.update1()
        
        screen.update2()
    return 0

def main() -> int:
    pygame.init()
    Online = client.Client(input())
    # Online = client.Client("13.76.138.194")
    room_list: list[Room] = []
    
    screen = Screen()
    # roomlist.append(Room("kitchen"), Room("bedroom"), Room("yard"),Room("study"), Room("liviingroom"))
    room_list.append(Room("kitchen", screen.info()))
    for room in room_list:
        room.data_update(Online.datas[room.name])
    running = True
    
    Online.send_data(cards=c.draw(Online.cards))
    
    while running == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
        
        screen.update1()
        
        screen.update2()
    return 0



if __name__ == "__main__":
    main()
