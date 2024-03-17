from os import path
import pygame

functional_cards = ("放置","謀殺", "布置現場","交易","足跡","拿取","檢視")

def draw_card(cards: list[str]) -> list[str]:
    hand.append(cards.pop())
    return cards


def deal_used_card():
    if inusing != None:
        inusing.ability()
    

class Card:
    def __init__(self, size: float, name: str, x: int=1 , y: int= 1) -> None:
        self.width = size
        self.height = size
        self.x = x
        self.y = y
        self.name = name
        self.imageOriginal = pygame.Surface((self.width,self.height))
        self.imageOriginal.fill((255,255,255))
        self.imageOriginal.blit(source = pygame.transform.scale(pygame.image.load(path.join("image/"+name+".png")).convert_alpha(),(180, 180)), dest = (0,0))
        self.imageOriginal.set_colorkey((255,255,255))
        self.image = self.imageOriginal.copy()

        self.ab = False
    def use(self, mouse_x, mouse_y):
            global inusing
            if self.touch(mouse_x, mouse_y) == 1:
                inusing = self  
                
    def update(self, surface: pygame.surface.Surface) -> None:
        self.draw(surface)

    def touch(self, mouse_x: int, mouse_y: int) -> int:
        if self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height:
            return 1
        else:
            return 0

    def draw(self, surface: pygame.surface.Surface):
        surface.blit(self.image, (self.x,self.y))
        
    def ability() -> None: ...


class Take(Card):
    def __init__(self, size: float, x: int=1, y: int=1) -> None:
        super().__init__(size, "拿取", x, y)
    
    def ability(self):
        ...
    
class Put_down(Card):
    def __init__(self, size: float, x: int=1, y: int=1) -> None:
        super().__init__(size, "放置", x, y)

    def ability(self):
        ...

class Kill(Card):  
    def __init__(self, size: float, x: int=1, y: int=1) -> None:
        super().__init__(size, "謀殺", x, y)
    def abiility(self):
        pass

class 


hand: list[Card] = []
items: list[Card] = []
feild: list[Card] = []
inusing: Card = None