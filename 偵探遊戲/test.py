class car:
    def __init__(self, wheel: int, color: str):
        self.wheel = wheel
        self.color = color
        
    
    def showcolor(self):
        print(self.color)
    

plane.showcolor()

plane = car(3, "red")
you = car(4, "green")

plane.showcolor()

plane.color = "blue"

plane.showcolor()
print("nunu")