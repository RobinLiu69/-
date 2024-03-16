from os import path
import pygame

cards = []
class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand_card = []
        self.hand_card.append(self)
    def remove():
        pass
    def add():
        pass
class Card:
    def __init__(self, size: float, name: str, x: float=1 , y: float= 1, owner: str="物品") -> None:
        self.width = size 
        self.height = size
        self.owner = owner
        self.x = x
        self.y = y
        self.name = name
        cards.append(self)
        self.imageOriginal = pygame.Surface((self.width,self.height))
        self.imageOriginal.fill((255,255,255))
        self.imageOriginal.blit(source = pygame.transform.scale(pygame.image.load(path.join("image/"+name+".png")).convert_alpha(),(180, 180)), dest = (0,0))
        self.imageOriginal.set_colorkey((255,255,255))
        self.image = self.imageOriginal.copy()
    
    
    def use(self):
        ...
    
    def update(self, surface: pygame.surface.Surface) -> None:
        self.draw(surface)

    def touch(self, mouse_x: int, mouse_y: int) -> int:
        if self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height:
            return 1
        else:
            return 0

    def draw(self, surface: pygame.surface.Surface):
        surface.blit(self.image, (self.x,self.y))

class Take(Card):
    def __init__(self, size: float, x: float=1, y: float=1, owner: str="物品") -> None:
        super().__init__(size, "拿取", x, y, owner)
    
    def ability(self):
        if self.owner == "":

