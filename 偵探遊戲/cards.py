from os import path
import pygame
import room as r

functional_cards = ("放置", "謀殺", "布置現場", "交易", "足跡", "拿取", "檢視")

def draw_card(cards: list[str], hand: list["Card"]) -> list[str]:
    hand.append(cards.pop())
    return cards, hand

# 做到一半
def init_card(cards: list[str], screen_info: tuple[int, int]) -> list["Card"]:
    temp = []
    for card in cards:
        print(f"{card}({screen_info[0]/10})", type(eval(f"{card}({screen_info[0]/10})")))
        temp.append(eval(f"{card}({screen_info[0]/10})"))
    return temp


class Card:
    def __init__(self, size: int, name: str, x: int=None , y: int=None) -> None:
        self.width = size
        self.height = size

        self.x = x
        self.y = y
        self.name = name
        self.imageOriginal = pygame.Surface((self.width,self.height))
        self.imageOriginal.fill((255,255,255))
        self.imageOriginal.blit(source = pygame.transform.scale(pygame.image.load(path.join("偵探遊戲/image/"+name+".png")).convert_alpha(),(self.width, self.height)), dest = (0,0))
        self.imageOriginal.set_colorkey((255,255,255))
        self.image = self.imageOriginal.copy()

        
    def update(self, surface: pygame.surface.Surface, screen_info: tuple[int, int], type: str, index: int=0, len: int=0) -> None:
        if type == "hand":
            self.x = screen_info[0]/(len+2)*index
            self.y = screen_info[1]/10*7
            self.draw(surface)
        # else:
        #     self.x = screen_info[0]/len*index
        #     self.y = screen_info[1]/10*9
        #     self.draw(surface)
        
        
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