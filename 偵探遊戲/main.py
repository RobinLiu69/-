import pygame
import client, server
import cards as c
import room as r
from os import path


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


def room_selection(screen: Screen, rooms: list[r.Room], room_map: r.Map, hand: list[str]) -> r.Room:
    nearst: r.Room = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("touch")
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
    
def enter_room(Online: client.Client, screen: Screen, room: r.Room, hand: list[str]) -> None:
    
    hand_card = c.init_card(hand, screen.info())
    item_card = c.init_card(room.items, screen.info())
    
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                    ...
        screen.fill()
        
        room.update(screen.screen, Online.datas[room.name])
        
        
        
        for index, card in enumerate(hand_card):
            card.update(screen.screen, screen.info(), "hand", index+1, len(hand_card))


        for index, card in enumerate(item_card):
            card.update(screen.screen, screen.info(), "item", index+1, len(item_card))

        screen.flip()
    return  None
    
def main() -> int:
    
    Online, rooms, screen = init()
    
    # roomlist.append(Room("kitchen"), Room("bedroom"), Room("yard"),Room("study"), Room("liviingroom"))
    rooms.append(r.Room("kitchen", screen.info(), screen.width*2/5, screen.height/16*11.5))
    
    room_map = r.Map(screen.info(), (screen.width, screen.height), rooms)
    
    for room in rooms:
        room.data_update(Online.datas[room.name])
        print(room.info())
        
    
    hand: list[str] = []
    
    
    try:
        for _ in range(5):
            cards, hand = c.draw_card(Online.cards, hand)
            Online.send_data(cards=cards)
    except:
        print("card list empty")
    
    
    # print("selecting rooms...")
    # the_room = room_selection(screen, rooms, room_map, hand)
    hand = ["Take", "Kill"]
    
    the_room = rooms[0]
    
    
    print("entering the room...")
    if the_room != None:
        enter_room(Online, screen, the_room, hand)



if __name__ == "__main__":
    main()