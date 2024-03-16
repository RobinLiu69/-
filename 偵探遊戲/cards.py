from os import path
import pygame
hand: list[str] = []
cards: list[str] = []


def draw(cards: list[str]) -> bool:
    hand.append(cards.pop())
    return cards
    

class Card:
    def __init__(self, size: float, name: str, x: int=1 , y: int= 1) -> None:
        self.width = size 
        self.height = size
        self.x = x
        self.y = y
        self.name = name
        cards.append(self)
        self.imageOriginal = pygame.Surface((self.width,self.height))
        self.imageOriginal.fill((255,255,255))
        self.imageOriginal.blit(source = pygame.transform.scale(pygame.image.load(path.join("image/"+name+".png")).convert_alpha(),(180, 180)), dest = (0,0))
        self.imageOriginal.set_colorkey((255,255,255))
        self.image = self.imageOriginal.copy()
<<<<<<< HEAD
    
    
    def use(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for i in c.cards:
            if i.touch(mouse_x, mouse_y) == 1:
                i.ability()
=======
        
    def use(self, mouse_x: int, mouse_y:int):
        if self.touch(mouse_x, mouse_y) == 1:
            self.ability()
            return 1
>>>>>>> 95fd81d (Co-authored-by: z9487xd <z9487xd@users.noreply.github.com>)
    
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
    
    def ability(self, data):
        pass
