import pygame, client
from os import path

class Room:
    def __init__(self, room_name: str, size: tuple[int, int], x: int, y: int) -> None:
        self.name = room_name
        self.x = x
        self.y = y
        self.items = []
        self.players = []
        self.width = size[0]
        self.height = size[1]
        self.imageOriginal = pygame.Surface((self.width, self.height))
        self.imageOriginal.fill((255,255,255))
        self.imageOriginal.blit(source = pygame.transform.scale(pygame.image.load(path.join("偵探遊戲/image/"+room_name+".png")).convert_alpha(),(180, 180)), dest = (0,0))
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
        
class Map:
    def __init__(self, screen_info: tuple[int, int]=(0, 0), size: tuple[int, int]=(0, 0), rooms: Room=None) -> None:
        self.x = screen_info[0]/2-size[0]
        self.y = screen_info[1]/2-size[1]
        self.width = size[0]
        self.height = size[1]
        self.room_list: list[Room] = rooms
        self.imageOriginal = pygame.Surface((self.width, self.height))
        self.imageOriginal.fill((255,255,255))
        self.imageOriginal.blit(source = pygame.transform.scale(pygame.image.load(path.join("偵探遊戲/image/地圖.png")).convert_alpha(),(180, 180)), dest = (0,0))
        self.imageOriginal.set_colorkey((255,255,255))
        self.image = self.imageOriginal.copy()

    def distance(self, x: int, y: int, room: Room) -> float:
        dx = x - room.x
        dy = y - room.y
        return (dx**2+dy**2)**0.5
    
    def update(self, surface: pygame.surface.Surface, data: client.Datas) -> None:
        self.draw(surface)
    
    def detect(self, x: int, y: int, screen_info: tuple[int, int]) -> Room:
        nearst = None
        for room in self.room_list:
            if nearst == None and self.distance(x, y, room) < screen_info[0]/100: nearst = room
            elif self.distance(x, y, room) < self.distance(x, y, nearst)  and self.distance(x, y, room) < screen_info[0]/100: nearst = room
        return nearst
        
    def draw(self, surface: pygame.surface.Surface) -> int:
        try:
            surface.blit(self.image, (self.x,self.y))
            return 0
        except Exception as e:
            print(e)
            return 1
