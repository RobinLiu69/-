import pygame
import client, server
import cards as c
import room as r
from os import path
from pwn import log



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
    Online = client.Client(input())
    screen = Screen()
    # Online = client.Client("13.76.138.194")
    rooms: list[r.Room] = []
    return Online, rooms, screen


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
        screen.fill()
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # print(mouse_x, mouse_y)
        nearst = room_map.detect(mouse_x, mouse_y, screen.info(), rooms, nearst)
        
        room_map.update(screen.screen)
        
        for room in rooms:
            room.drawC(screen.screen, screen.width)
        
        screen.flip()
    return nearst
    
def enter_room(Online: client.Client, screen: Screen, room: r.Room, hand: list[tuple[str, int]]) -> None:
    
    hand_card = c.init_card(hand, screen.info())
    item_card = c.init_card(room.items, screen.info())
    
    using_card: c.Card = None
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if using_card == None:
                    for card in hand_card+item_card:
                        if card.touching:
                            using_card = card
                            using_card.using = True
                            break
                else:
                    for card in hand_card+item_card:
                        if card.touching and card != using_card:
                            if using_card.ability(card, hand, room.items):
                                using_card.using = False
                                using_card = None
                                hand_card = c.init_card(hand, screen.info())
                                item_card = c.init_card(room.items, screen.info())
                                room.change(Online)
                            else:
                                using_card.using = False
                                using_card = None
                            break
                        elif card.touching and card == using_card:
                            using_card.using = False
                            using_card = None
                            break
        
        # hand_card = c.init_card(hand, screen.info())
        # item_card = c.init_card(room.items, screen.info())
        
        screen.fill()
        
        for card in item_card:
            for value in room.items:
                if card.identity == value[1]:
                    break
            else:
                print("update")
                item_card = c.init_card(room.items, screen.info())
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        room.update(screen.screen, Online.datas[room.name])
        
        
        for index, card in enumerate(hand_card):
            card.update(screen.screen, screen.info(), "hand", index+1, len(hand_card), mouse_x, mouse_y)
            

        for index, card in enumerate(item_card):
            card.update(screen.screen, screen.info(), "item", index+1, len(item_card), mouse_x, mouse_y)

        screen.flip()
    return  None
    
def main() -> int:
    
    Online, rooms, screen = init()
    
    # roomlist.append(Room("kitchen"), Room("bedroom"), Room("yard"),Room("study"), Room("liviingroom"))
    rooms.append(r.Room("kitchen", screen.info(), screen.width*2/5, screen.height/16*11.5))
    # rooms.append(r.Room("bedroom", screen.info(), screen.width*2/5, screen.height/16*11.5))
    # rooms.append(r.Room("yard",    en.info(), screen.width*2/5, screen.height/16*11.5))
    # rooms.append(r.Room("study", screen.info(), screen.width*2/5, screen.height/16*11.5))
    # rooms.append(r.Room("livingroom", screen.info(), screen.width*2/5, screen.height/16*11.5))
    
    room_map = r.Map(screen.info(), (screen.width, screen.height), rooms)
    
    for room in rooms:
        room.data_update(Online.datas[room.name])
        print(room.info())
        
    
    hand: list[tuple[str, int]] = []
    
    
    try:
        for _ in range(5):
            cards, hand = c.draw_card(Online.cards, hand)
            Online.send_data(cards=cards)
    except:
        log.success("card list empty")
    
    hand: list[tuple[str, int]] = [("Take", 100), ("Take", 102), ("Take", 101), ("Take", 103)]
    
    
    log.success("selecting rooms...")
    the_room = room_selection(screen, rooms, room_map, hand)
    
    the_room = rooms[0]
    

    log.success("entering the room...")
    if the_room != None:
        enter_room(Online, screen, the_room, hand)



if __name__ == "__main__":
    main()
