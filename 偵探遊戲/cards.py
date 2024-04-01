from os import path
import pygame

functional_cards = ("放置", "謀殺", "佈置現場", "交易", "足跡", "拿取", "檢視")

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
        super().__init__(size, "Take", x, y)#拿取

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        if len(selected_cards) > 1: return 0
        selected_card = selected_cards[0]
        if selected_card in items and selected_card.name not in functional_cards:
            items.remove(selected_card)
            hand.append(selected_card)
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
        super().__init__(size, "Put_down", x, y)#放置

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        if len(selected_cards) > 1: return 0
        selected_card = selected_cards[0]
        if selected_card in hand and selected_card.name not in functional_cards:
            hand.remove(selected_card)
            items.append(selected_card)
        else:
            return 0
        if self in hand:
            hand.remove(self)
            items.append(self)
        else:
            return 0
        return 1
    
class Swap(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Swap", x, y)#交換

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        if len(selected_cards) > 2 or len(selected_cards) < 2: return 0
        card_1, card_2 = selected_cards[0], selected_cards[1]
        if card_1 in items:
            index_1 = items.index(card_1)
        else:
            return 0
        if card_2 in items:
            index_2 = items.index(card_2)
        else:
            return 0
        items[index_1], items[index_2] = items[index_2], items[index_1]
        if self in hand:
            hand.remove(self)
            items.append(self)
        else:
            return 0
        return 1

class Kill(Card):  
    def __init__(self, size: float, x: int=1, y: int=1) -> None:
        super().__init__(size, "Kill", x, y)

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...


class Trade(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Trade", x, y)#交易

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class View(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "View", x, y)#檢視

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Footprints(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Footprints", x, y)#足跡

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Chandelier(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Chandelier", x, y)#"吊燈"

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Pot(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Pot", x, y)#空的盆栽

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Footprints(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "交易", x, y)

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Remote_control(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Remote_control", x, y)#姚控器

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Pistol(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Pistol", x, y)#手槍

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Bullet(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Bullet", x, y)#彈殼

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Pillow(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Pillow", x, y)#枕頭

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Safe(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Safe", x, y)#安全

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Rag(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Rag", x, y)#抹布

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Kinfe(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Kinfe", x, y)#菜刀

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Frozen_Pork(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Pork", x, y)#冷凍豬肉

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Flowers(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Flowers", x, y)#"花叢"

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Water(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Water", x, y)#水

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Garden_shear(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Garden_shear", x, y)#園藝剪

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Monitor(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Monitor", x, y)#監視器

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Key(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Key", x, y)#鑰匙

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Pen(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Pen", x, y)#鋼筆

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Unused_mask(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Unused_mask", x, y)#未使用的易容面具

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Tracker(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Tracker", x, y)#追蹤器

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Whisky(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Whisky", x, y)#威士��

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Flashlight(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Flashlight", x, y)#手電筒

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Rope(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Rope", x, y)#繩子

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Mud(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Mud", x, y)#泥巴

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Bugging_receiver(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Bugging_receiver", x, y)#竊聽筒

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Cross(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Cross", x, y)#十字架

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Broom(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Broom", x, y)#掃把

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Coffee_pot(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Coffee_pot", x, y)#咖啡壺

    def ability(self, selected_cards: list[Card], hand: list[Card], items: list[Card]) -> int:
        ...

class Bloody_garden_shear(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Bloody_garden_shear", x, y)#血剪

    def ability(self, selected_Card: Card, hand: list[Card], items: list[Card], mouse_x: int = None, mouse_y: int = None) -> int:
        ...

class Bloody_knife(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Bloody_knife", x, y)#血刀

    def ability(self, selected_Card: Card, hand: list[Card], items: list[Card], mouse_x: int = None, mouse_y: int = None) -> int:
        ...

class Bloody_pen(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Bloody_pen", x, y)#血鋼筆

    def ability(self, selected_Card: Card, hand: list[Card], items: list[Card], mouse_x: int = None, mouse_y: int = None) -> int:
        ...

class Broken_cross(Card):
    def __init__(self, size: int, x: int=1, y: int=1) -> None:
        super().__init__(size, "Broken_cross", x, y)#破十字架

    def ability(self, selected_Card: Card, hand: list[Card], items: list[Card], mouse_x: int = None, mouse_y: int = None) -> int:
        ...