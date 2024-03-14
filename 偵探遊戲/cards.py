from os import path
import pygame


class Cards:
    def __init__(self, size: float, name: str, x: float=1 , y:float= 1, owner:str = "物品") -> None:
        self.width = size 
        self.height = size
        self.owner = owner
        self.x = x
        self.y = y
        self.name = name

        self.imageOriginal = pygame.Surface((self.width,self.height))
        self.imageOriginal.fill((255,255,255))
        self.imageOriginal.blit(source = pygame.transform.scale(pygame.image.load(path.join("image/"+name+".png")).convert_alpha(),(180, 180)), dest = (0,0))
        self.imageOriginal.set_colorkey((255,255,255))
        self.image = self.imageOriginal.copy()
    
    def ability(self):
        ...
    
    def use(self):
        ...
    
    def update(self, surface: pygame.surface.Surface) -> None:
        self.draw(surface)
        

    def touch(self, x: int, y: int) -> bool:
        
        return True

    def draw(self, surface: pygame.surface.Surface):
        surface.blit(self.image, (self.x,self.y))


class Ability:
    def __init__(self, name: str):
            self.name = name
            
    