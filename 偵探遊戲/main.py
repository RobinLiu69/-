import pygame
import client, server
from cards import *
import room as r
from os import path
from pwn import log
import time



class Player:
    def __init__(self, name: str, server_address: str, hand: list[Card]=[], x: int = 1, y: int = 1, size: int = 1):
        self.name = name
        self.hand = hand
        self.Online = client.Client(server_address)
        self.width = size
        self.height = size
        self.x = x
        self.y = y
        # self.imageOriginal = pygame.Surface((self.width,self.height))
        # self.imageOriginal.fill((255,255,255))
        # self.imageOriginal.blit(source = pygame.transform.scale(pygame.image.load(path.join("偵探遊戲/image/"+name+".png")).convert_alpha(),(self.width, self.height)), dest = (0,0))
        # self.imageOriginal.set_colorkey((255,255,255))
        # self.image = self.imageOriginal.copy()
    def update(self, surface):
        self.draw(surface)

    def draw(self, surface: pygame.surface.Surface):
        surface.blit(self.image, (self.x,self.y)) 

    def selected(self):
        ...

# 偵探：遊戲開始獲得一張簡視
# 園丁：將花朵放置於盆栽
# 廚師：持有解凍肉及菜刀
# 火雞：持有三種以上的凶器
class Detective(Player):
    def __init__(self, size: int, x: int = 1, y: int = 1) -> None:
        super().__init__("Detective", size, x, y)

    def ability(self) -> int:
        ...

class Gardener(Player):
    def __init__(self, size: int, x: int = 1, y: int = 1) -> None:
        super().__init__("Gardener", size, x, y)

    def ability(self) -> int:
        ...

class Cheif(Player):
    def __init__(self, size: int, x: int = 1, y: int = 1) -> None:
        super().__init__("Cheif", size, x, y)

    def ability(self) -> int:
        ...

class Firechicken(Player):
    def __init__(self, size: int, x: int = 1, y: int = 1) -> None:
        super().__init__("Firechicken", size, x, y)

    def ability(self) -> int:
        ...


class Screen:
    def __init__(self, width: int=None, height: int=None) -> None:
        self.width, self.height = width, height
        self.width, self.height = self.info()
        print(self.width, self.height)
        if self.width/self.height != 1.6:
            self.resize()
        self.screen = pygame.display.set_mode((self.width, self.height))
        print(self.width, self.height)
        pygame.display.set_caption("Detective Game")
    
    def resize(self):
        for i in range(1000, self.width):
            for j in range(900, self.height):
                if i/j == 1.6:
                    self.width, self.height = i, j


    def info(self) -> tuple[int, int]:
        try:
            return self.width//1, self.height//1
        except:
            return pygame.display.get_desktop_sizes().pop()
        
        
    def fill(self) -> None:
        self.screen.fill((0, 0, 0))
    
    def flip(self) -> None:
        pygame.display.flip()

def init():
    pygame.init()
    player = Player("robin", input("Server address: "))
    screen = Screen()
    # Online = client.Client("13.76.138.194")
    rooms: list[r.Room] = []
    return player, rooms, screen


def room_selection(screen: Screen, rooms: list[r.Room], room_map: r.Map, hand: list[tuple[str, int]]) -> r.Room:
    nearst: r.Room = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("clicked")
                if nearst != None:
                    running = False
                    
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            running = False
            
        screen.fill()
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # print(mouse_x, mouse_y)
        nearst = room_map.detect(mouse_x, mouse_y, screen.info(), rooms, nearst)
        
        room_map.update(screen.screen)
        
        for room in rooms:
            room.drawC(screen.screen, screen.width)
        
        screen.flip()
    return nearst
    
def enter_room(player: Player, screen: Screen, room: r.Room) -> None:
    
    using_card: Card = None
    
    cards: list[Card] = []
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if using_card == None:
                    for card in player.hand:
                        if card.touching:
                            using_card = card
                            using_card.using = True
                            break
                else:
                    for card in player.hand+room.items:
                        if card.touching and card != using_card and card not in cards:
                            card.using = True
                            cards.append(card)
                        elif card.touching and card != using_card and card in cards:
                            card.using = False
                            cards.remove(card)
                        elif card.touching and card == using_card:
                            using_card.using = False
                            using_card = None
                            for card in cards: card.using = False
                            cards.clear()
                            break
                    if using_card != None and abs(using_card.ability(cards, player.hand, room.items)):
                        print("change")
                        print(cards)
                        using_card.using = False
                        using_card = None
                        for card in cards: card.using = False
                        cards.clear() 
                        room.change(player.Online)
                        room.data_update(player.Online.datas, screen.info())
                       

        # hand_card = init_card(hand, screen.info())
        # item_card = init_card(room.items, screen.info())
        
        keys = pygame.key.get_pressed()
        
        
        if keys[pygame.K_BACKSPACE]:
            running = False
        
        screen.fill()
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        room.update(screen.screen, player.Online.datas[room.name], screen.info())
        
        
        for index, card in enumerate(player.hand):
            card.update(screen.screen, screen.info(), "hand", index+1, len(player.hand), mouse_x, mouse_y)
            

        for index, card in enumerate(room.items):
            card.update(screen.screen, screen.info(), "item", index+1, len(room.items), mouse_x, mouse_y)

        screen.flip()
    return  None
    
def initial_room(rooms: list[r.Room], player: Player, screen: Screen) -> int:
    try:
        for room in rooms:
            room.data_update(player.Online.datas[room.name], screen.info())
        else:
            return 0
    except Exception as e:
        print("key error: ", e)
        return 1

def main() -> int:
    
    player, rooms, screen = init()
    
    # roomlist.append(Room("kitchen"), Room("bedroom"), Room("yard"),Room("study"), Room("liviingroom"))
    rooms.append(r.Room("kitchen", screen.info(), screen.width*2/5, screen.height/16*11.5))
    rooms.append(r.Room("yard", screen.info(), screen.width*11.75/16, screen.height/2)) # yard
    rooms.append(r.Room("livingroom", screen.info(), screen.width*0.42, screen.height*0.45)) # livingroom
    rooms.append(r.Room("study", screen.info(), screen.width/4, screen.height*2/5)) # study
    rooms.append(r.Room("bedroom", screen.info(), screen.width*4/7, screen.height*0.26)) # bedroom
    
    room_map = r.Map(screen.info(), (screen.width, screen.height), rooms)
    while initial_room(rooms, player, screen):
        print("Error when getting room's data...")
        print("Retrying...")
        time.sleep(1)
        
    running = True
    
    
    while running:
        try:
            for _ in range(5):
                cards, player.hand = draw_card(player.Online.cards, player.hand)
                player.Online.send_data(cards=cards)
        except:
            log.success("Card list empty")
        
        player.hand = init_card(list(map(client.Items, ["Take", "Take", "Put_down", "Put_down", "Swap", "Swap", "Rag", "Pistol"])), screen.info())
        
        log.success("Selecting rooms...")
        the_room = room_selection(screen, rooms, room_map, player)
        
        for room in rooms:
            room.hightlight = False
        

        log.success("Entering the room...")
        if the_room != None:
            enter_room(player, screen, the_room)
        else:
            log.success("No room selected")
            running = False

    return 0


if __name__ == "__main__":
    main()
    log.success("Quit")
    pygame.quit()
    
