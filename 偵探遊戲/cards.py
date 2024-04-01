from os import path
import pygame

functional_cards = ("放置", "謀殺", "布置現場", "交易", "足跡", "拿取", "檢視")

def draw_card(cards: list[str], hand: list["Card"], screen_info: tuple[int, int]) -> tuple[list[str], list["Card"]]:
    hand += init_card(cards.pop(), screen_info)
    return cards, hand

# 做到一半
def init_card(cards: list["Card"], screen_info: tuple[int, int]) -> list["Card"]:
    temp = []
    for card in cards:
        # print(f"{card}({screen_info[0]/10})", type(eval(f"{card}({screen_info[0]/10})")))
        temp.append(eval(f"{card}({screen_info[0]/10})"))
    return temp


class Card:
    def __init__(self, size: int, name: str, x: int=None , y: int=None) -> None:
        self.width = size
        self.height = size
        self.x = x
        self.y = y
        self.name = name
        self.touching = False
        self.using = False
        self.imageOriginal = pygame.Surface((self.width,self.height))
        self.imageOriginal.fill((255,255,255))
        self.imageOriginal.blit(source = pygame.transform.scale(pygame.image.load(path.join("偵探遊戲/image/"+name+".png")).convert_alpha(),(self.width, self.height)), dest = (0,0))
        self.imageOriginal.set_colorkey((255,255,255))
        self.image = self.imageOriginal.copy()
        
    def update(self, surface: pygame.surface.Surface, screen_info: tuple[int, int], type: str, index: int=0, len: int=0, mouse_x: int=0, mouse_y: int=0) -> None:
        self.touching = self.touch(mouse_x, mouse_y)
        if type == "hand":
            self.x = screen_info[0]//2 - self.width*1.1*(1+len//2) + self.width*1.1*index
            if self.touching or self.using: self.y = screen_info[1]/10*7 - self.height*0.3
            else: self.y = screen_info[1]/10*7
            self.draw(surface)
        elif type == "item":
            yp = (index-1)//5
            self.x = screen_info[0]//2 - self.width*1.2*2.5 + self.width*1.2*((index-1)%5)
            if self.touching or self.using: self.y = screen_info[1]/10 + self.height*1.1*(yp) - self.height*0.3
            else: self.y = screen_info[1]/10 + self.height*1.1*(yp)
            self.draw(surface)
        
        
    def touch(self, mouse_x: int, mouse_y: int) -> int:
        if not self.touching and self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height*1: return 1
        if self.touching and self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height*1.3: return 1
        else: return 0
    
    def detect(self, mouse_x: int, mouse_y: int) -> bool:
        if self.touch(mouse_x, mouse_y):
            return True
        else:
            return False

    def use(self, mouse_x: int, mouse_y: int, using: bool):
      if self.touch(mouse_x, mouse_y) == 1 and using == False:
            using = True
            self.y += 15

    def draw(self, surface: pygame.surface.Surface):
        surface.blit(self.image, (self.x,self.y))
        
    def ability() -> None: ...


class Take(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "拿取", x, y)

    def ability(self, selected_Card: Card, hand: list[Card], items: list[Card]) -> int:
        if selected_Card in items and selected_Card.name not in functional_cards:
            items.remove(selected_Card)
            hand.append(selected_Card)
        else:
            return 0
        if self in hand:
            hand.remove(self)
            items.append(self)
        else:
            return 0
        return 1
        
       
        
    
class Put_down(Card):
    def __init__(self, size: float, x: int=1, y: int=1) -> None:
        super().__init__(size, "放置", x, y)

    def ability(self, selected_Card: Card, hand: list[Card], items: list[Card]) -> int:
        if selected_Card in hand and selected_Card.name not in functional_cards:
            hand.remove(selected_Card)
            items.append(selected_Card)
        else:
            return 0
        if self in hand:
            hand.remove(self)
            items.append(self)
        else:
            return 0
        return 1

class Kill(Card):  
    def __init__(self, size: float, x: int=1, y: int=1) -> None:
        super().__init__(size, "謀殺", x, y)
    def abiility(self):
        pass

class Swap(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "布置現場", x, y)

    def ability(self):
        ...

class Trade(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "交易", x, y)

    def ability(self):
        ...

class View(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "檢視", x, y)

    def ability(self):
        ...

class Footprints(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "足跡", x, y)

    def ability(self):
        ...

class Chandelier(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "吊燈", x, y)

    def ability(self):
        ...

class Pot(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "空的盆栽", x, y)

    def ability(self):
        ...

class Footprints(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "交易", x, y)

    def ability(self):
        ...

class Remote_control(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "遙控器", x, y)

    def ability(self):
        ...

class Pistol(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "手槍", x, y)

    def ability(self):
        ...

class Bullet(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "彈殼", x, y)

    def ability(self):
        ...

class Pillow(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "枕頭", x, y)

    def ability(self):
        ...

class Safe(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "保險箱", x, y)

    def ability(self):
        ...

class Rag(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "抹布", x, y)

    def ability(self):
        ...

class Kinfe(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "菜刀", x, y)

    def ability(self):
        ...

class Pork(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "冷凍豬肉", x, y)

    def ability(self):
        ...

class Flowers(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "花叢", x, y)

    def ability(self):
        ...

class Water(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "水", x, y)

    def ability(self):
        ...

class Garden_shears(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "園藝剪", x, y)

    def ability(self):
        ...

class Monitor(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "監視器", x, y)

    def ability(self):
        ...

class Key(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "鑰匙", x, y)

    def ability(self):
        ...

class Pen(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "鋼筆", x, y)

    def ability(self):
        ...

class Unused_mask(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "未使用的易容面具", x, y)

    def ability(self):
        ...

class Tracker(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "追蹤器", x, y)

    def ability(self):
        ...

class Whisky(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "威士忌", x, y)

    def ability(self):
        ...

class Flashlight(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "手電筒", x, y)

    def ability(self):
        ...

class Rope(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "繩子", x, y)

    def ability(self):
        ...

class Mud(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "泥巴", x, y)

    def ability(self):
        ...

class Bugging_receiver(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "竊聽筒", x, y)

    def ability(self):
        ...

class Cross(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "十字架", x, y)

    def ability(self):
        ...

class Broom(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "掃把", x, y)

    def ability(self):
        ...

class Coffee_pot(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "咖啡壺", x, y)

    def ability(self):
        ...



