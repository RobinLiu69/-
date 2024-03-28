from os import path
import pygame

functional_cards = ("放置", "謀殺", "布置現場", "交易", "足跡", "拿取", "檢視")

def draw_card(cards: list[str], hand: list["Card"]) -> list[str]:
    hand.append(cards.pop())
    return cards, hand

# 做到一半
# def init_card(: list[str]):
#     room_card = []
#     for card in hand:
#         room_card.append(card)


class Card:
    def __init__(self, size: int, name: str, x: int=1 , y: int=1) -> None:
        self.width = size
        self.height = size

        self.x = x
        self.y = y
        self.name = name
        self.imageOriginal = pygame.Surface((self.width,self.height))
        self.imageOriginal.fill((255,255,255))
        self.imageOriginal.blit(source = pygame.transform.scale(pygame.image.load(path.join("偵探遊戲/image/"+name+".png")).convert_alpha(),(180, 180)), dest = (0,0))
        self.imageOriginal.set_colorkey((255,255,255))
        self.image = self.imageOriginal.copy()

        
    # def use(self, mouse_x, mouse_y):
    #         global inusing, path         
    #         if self.touch(mouse_x, mouse_y) == 1:
    #             inusing = self 
    #             for times in range(20):
    #                 self.y += 1
                
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
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
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

inusing: Card = None