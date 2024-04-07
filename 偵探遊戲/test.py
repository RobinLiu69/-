# int str float complex bool
a: int = 10
b: str = "pp"
c: float = 10.0
d: complex = 10+10j
f: bool = True

i = int()

def score_check(score):
    if score >= 60:
        print("you passed")
    else:
        print("you didn't pass")
        
import numpy as np

# iterable: str list tuple dict set
s: str = "abcd"
s.split()

l: list[int] = [10, 5, 8]
l.append(5) # method
l.remove(5)
l.pop(0)
# d[100] = 10

t: tuple[int] = (10, 5)


d: dict[str, str] = {"香蕉": "banana"}
d["apple"] = "蘋果"

se: set = {10, 10, 4, 5, 5, 5, 5, 5}

sum = 0
for i in range(5):
    sum += i

i = 0
while i < 5:
    i += 1
    if i % 2 == 0:
        pass
        # break continue
    # print(i)

class player:
    def __init__(self, hp: int, atk: int):
        self.hp = hp
        self.atk = atk
        
    def hpcheck(self, other: "player"):
        if other.hp > self.hp : print("your hp lower than the other player")
        else: print("your hp higher than the other player")

my = player(5, 5)
you = player(7, 7)

my.hpcheck(you)
