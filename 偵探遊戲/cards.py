from os import path
import pygame
import room as r

functional_cards = ("放置", "謀殺", "布置現場", "交易", "足跡", "拿取", "檢視")

def draw_card(cards: list[tuple[str, int]], hand: list[tuple[str, int]]) -> tuple[list[tuple[str, int]], list[tuple[str, int]]]:
    hand.append(tuple(cards.pop()))
    return cards, hand

# 做到一半
def init_card(cards: list[tuple[str, int]], screen_info: tuple[int, int]) -> list["Card"]:
    temp = []
    for card in cards:
        # print(f"{card}({screen_info[0]/10})", type(eval(f"{card}({screen_info[0]/10})")))
        temp.append(eval(f"{card[0]}({screen_info[0]/10}, identity={card[1]})"))
    return temp


class Card:
    def __init__(self, size: int, name: str, x: int=None , y: int=None, identity: int=0) -> None:
        self.width = size
        self.height = size
        self.x = x
        self.y = y
        self.name = name
        self.touching = False
        self.using = False
        self.identity = identity
        self.imageOriginal = pygame.Surface((self.width,self.height))
        self.imageOriginal.fill((255,255,255))
        self.imageOriginal.blit(source = pygame.transform.scale(pygame.image.load(path.join("偵探遊戲/image/"+name+".png")).convert_alpha(),(self.width, self.height)), dest = (0,0))
        self.imageOriginal.set_colorkey((255,255,255))
        self.image = self.imageOriginal.copy()
        
    def update(self, surface: pygame.surface.Surface, screen_info: tuple[int, int], type: str, index: int=0, len: int=0, mouse_x: int=0, mouse_y: int=0) -> None:
        self.touching = self.touch(mouse_x, mouse_y)
        if type == "hand":
            self.x = screen_info[0]//2 - self.width*1.1*(1+len//2) + self.width*1.1*index
            if self.touching or self.using: self.y = screen_info[1]/10*7 - self.height*0.6
            else: self.y = screen_info[1]/10*7
            self.draw(surface)
        elif type == "item":
            yp = (index-1)//5
            self.x = screen_info[0]//2 - self.width*1.2*2.5 + self.width*1.2*((index-1)%5)
            if self.touching or self.using: self.y = screen_info[1]/10 + self.height*1.1*(yp) - self.height*0.6
            else: self.y = screen_info[1]/10 + self.height*1.1*(yp)
            self.draw(surface)
        
        
    def touch(self, mouse_x: int, mouse_y: int) -> int:
        if not self.touching and self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height*1: return 1
        if self.touching and self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height*1.6: return 1
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
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "拿取", x, y, identity)

    def ability(self, selected_Card: Card, hand: list[tuple[str, int]], items: list[tuple[str, int]]) -> int:
        for index, card in enumerate(items):
            if card[1] == selected_Card.identity:
                hand.append(items.pop(index))
                break
        else:
            print("out")
            return 0
        for index, card in enumerate(hand):
            if self.identity == card[1]:
                items.append(hand.pop(index))
                break
        else:
            return 0
        return 1
        
        
    
class Put_down(Card):
    def __init__(self, size: float, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "放置", x, y, identity)

    def ability(self):
        ...

class Kill(Card):  
    def __init__(self, size: float, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "謀殺", x, y, identity)
    def abiility(self):
        pass

class Swap(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "布置現場", x, y, identity)

    def ability(self):
        ...

class Trade(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "交易", x, y, identity)

    def ability(self):
        ...

class View(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "檢視", x, y, identity)

    def ability(self):
        ...

class Footprints(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "足跡", x, y, identity)

    def ability(self):
        ...

class Chandelier(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "吊燈", x, y, identity)

    def ability(self):
        ...

class Pot(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "空的盆栽", x, y, identity)

    def ability(self):
        ...

class Footprints(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "交易", x, y, identity)

    def ability(self):
        ...

class Remote_control(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "遙控器", x, y, identity)

    def ability(self):
        ...

class Pistol(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "手槍", x, y, identity)

    def ability(self):
        ...

class Bullet(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "彈殼", x, y, identity)

    def ability(self):
        ...

class Pillow(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "枕頭", x, y, identity)

    def ability(self):
        ...

class Safe(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "保險箱", x, y, identity)

    def ability(self):
        ...

class Rag(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "抹布", x, y, identity)

    def ability(self):
        ...

class Kinfe(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "菜刀", x, y, identity)

    def ability(self):
        ...

class Pork(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "冷凍豬肉", x, y, identity)

    def ability(self):
        ...

class Flowers(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "花叢", x, y, identity)

    def ability(self):
        ...

class Water(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "水", x, y, identity)

    def ability(self):
        ...

class Garden_shears(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "園藝剪", x, y, identity)

    def ability(self):
        ...

class Monitor(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "監視器", x, y, identity)

    def ability(self):
        ...

class Key(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "鑰匙", x, y, identity)

    def ability(self):
        ...

class Pen(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "鋼筆", x, y, identity)

    def ability(self):
        ...

class Unused_mask(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "未使用的易容面具", x, y, identity)

    def ability(self):
        ...

class Tracker(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "追蹤器", x, y, identity)

    def ability(self):
        ...

class Whisky(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "威士忌", x, y, identity)

    def ability(self):
        ...

class Flashlight(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "手電筒", x, y, identity)

    def ability(self):
        ...

class Rope(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "繩子", x, y, identity)

    def ability(self):
        ...

class Mud(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "泥巴", x, y, identity)

    def ability(self):
        ...

class Bugging_receiver(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "竊聽筒", x, y, identity)

    def ability(self):
        ...

class Cross(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "十字架", x, y, identity)

    def ability(self):
        ...

class Broom(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "掃把", x, y, identity)

    def ability(self):
        ...

class Coffee_pot(Card):
    def __init__(self, size: int, x: int=1, y: int=1, identity: int=0) -> None:
        super().__init__(size, "咖啡壺", x, y, identity)

    def ability(self):
        ...



