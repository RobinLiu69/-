import pygame, client
from os import path
from cards import *

class Room:
    def __init__(self, room_name: str, size: tuple[int, int], x: int, y: int) -> None:
        self.name = room_name
        self.x = x
        self.y = y
        self.items: list[Card] = []
        self.players = []
        self.width = size[0]
        self.height = size[1]
        self.hightlight = False
        self.imageOriginal = pygame.Surface((self.width, self.height))
        self.imageOriginal.fill((255,255,255))
        self.imageOriginal.blit(source = pygame.transform.scale(pygame.image.load(path.join("偵探遊戲/image/"+room_name+".png")).convert_alpha(), size), dest = (0,0))
        self.imageOriginal.set_colorkey((255,255,255))
        self.image = self.imageOriginal.copy()
        
    def drawC(self, surface: pygame.surface.Surface, height: int) -> None:
        if not self.hightlight:
            pygame.draw.circle(surface, (100, 100, 10), (self.x, self.y), height/100)
        else:
            pygame.draw.circle(surface, (150, 150, 10), (self.x, self.y), height/50)
    
    def update(self, surface: pygame.surface.Surface, data: client.Datas, screen_info: tuple[int, int]) -> None:
        self.draw(surface)
        if self.changed(data):
            self.data_update(data, screen_info)
    
    def changed(self, data: client.Datas) -> int:
        temp: list[str] = [card.__class__.__name__ for card in self.items]
        if temp != data.items:
            return 1
        elif self.players != data.players: return 1
        else: return 0
    
    def change(self, online: client.Client):
        online.send_data(self.name, [card.__class__.__name__ for card in self.items], self.players)
    
    def data_update(self, data: client.Datas, screen_info: tuple[int, int]) -> int:
        try:
            self.items: list[Card] = init_card(data.items, screen_info)
            self.players: list[str] = data.players
            return 0
        except Exception as e:
            print(e)
            return 1
    
    def info(self) -> tuple[str, list[str], list[str]]:
        return self.name, self.items, self.players
        
    def draw(self, surface: pygame.surface.Surface) -> int:
        try:
            surface.blit(self.image, (0, 0))
            return 0
        except Exception as e:
            print(f"room draw:{e}")
            return 1
        
class Map:
    def __init__(self, screen_info: tuple[int, int]=(0, 0), size: tuple[int, int]=(0, 0), rooms: Room=None) -> None:
        self.x = screen_info[0]/2-size[0]*2/5
        self.y = screen_info[1]/2-size[1]*2/5
        self.width = size[0]
        self.height = size[1]
        
        self.imageOriginal = pygame.Surface((self.width, self.height))
        self.imageOriginal.fill((255, 255, 255))
        self.imageOriginal.blit(source = pygame.transform.scale(pygame.image.load(path.join("偵探遊戲/image/地圖.png")).convert_alpha(),(size[0]*4/5, size[1]*4/5)), dest = (0,0))
        self.imageOriginal.set_colorkey((255, 255, 255))
        self.image = self.imageOriginal.copy()

    def distance(self, x: int, y: int, room: Room) -> float:
        dx = x - room.x
        dy = y - room.y
        return (dx**2+dy**2)**0.5
    
    def update(self, surface: pygame.surface.Surface) -> None:
        self.draw(surface)
    
    def detect(self, x: int, y: int, screen_info: tuple[int, int], rooms: list[Room], nearst: Room=None) -> Room:
        for room in rooms:
            if nearst == None and self.distance(x, y, room) < screen_info[0]/50:
                nearst = room
                nearst.hightlight = True
            elif nearst != None and self.distance(x, y, room) < self.distance(x, y, nearst)  and self.distance(x, y, room) < screen_info[0]/50:
                nearst.hightlight = False
                nearst = room
                nearst.hightlight = True
                
        if nearst != None and self.distance(x, y, nearst) > screen_info[0]/50:
            nearst.hightlight = False
            nearst = None
        
        return nearst
        
    def draw(self, surface: pygame.surface.Surface) -> int:
        try:
            surface.blit(self.image, (self.x, self.y))
            return 0
        except Exception as e:
            print(e)
            return 1
