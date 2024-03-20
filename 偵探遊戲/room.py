import pygame, client
from os import path

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