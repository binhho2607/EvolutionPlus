#from Organism import *

import random
import math
class Organism(object):
    def __init__(self, cx, cy, speed, size, sense, data, energy = 20, generation = 1):
        self.cx = cx
        self.cy = cy
        self.speed = speed
        self.size = size
        self.sense = sense
        self.energy = energy
        self.dx = random.choice([1,0,-1])
        self.dy = random.choice([1,0,-1])
        self.foundFood = False
        self.age = 0
        self.reproduceDelay = 0
        self.chanceDie = data.percentDie
        self.foundMate = False
        self.mate = None
        self.fightDelay = 0
        self.generation = generation
        self.offsprings = 0

    def move(self, data):
        self.reactToWall(data)
        if self.foundFood == False and self.foundMate == False: #found food = not change direction
            chance = 10
            #change direction by chance
            if random.randint(1,100) <= chance:
                tempDx = self.dx
                tempDy = self.dy
                while tempDx == self.dx:
                    tempDx = random.choice([1,0,-1])
                if tempDx == 0:
                    while tempDy == self.dy:
                        tempDy = random.choice([1,-1])
                else:
                    while tempDy == self.dy:
                        tempDy = random.choice([1,0,-1])
                self.dx = tempDx
                self.dy = tempDy
        self.cx = self.cx + self.speed*3*self.dx
        self.cy = self.cy + self.speed*3*self.dy

    def reactToWall(self, data):
        if self.cx-self.size*10 < 0 or self.cx+self.size*10 > data.width:
            # tempDx = self.dx
            # while tempDx == self.dx:
            #     tempDx = random.choice([1,0,-1])
            # self.dx = tempDx
            self.dx *= -1
            if self.cx-self.size*10 < 0:
                self.cx = 0+self.size*10
            else:
                self.cx = data.width - self.size*10
        if self.cy-self.size*10 < 0 or self.cy+self.size*10 > data.height:
            # tempDy = self.dy
            # while tempDy == self.dy:
            #     tempDy = random.choice([1,0,-1])
            # self.dy = tempDy
            self.dy*=-1
            if self.cy-self.size*10 < 0:
                self.cy = 0+self.size*10
            else:
                self.cy = data.height - self.size*10

    def headToFood(self, other):
        if self.foundMate == False:
            self.foundFood = True
            xDist = other.cx - self.cx
            yDist = other.cy - self.cy
            #print("distances",xDist, yDist)
            if xDist == 0:
                if yDist > 0:
                    self.dy = abs(self.speed)
                else:
                    self.dy = abs(self.speed)*(-1)
                return
            angle = math.atan(yDist/xDist)
            if other.cx < self.cx:
                factor = -1
            else:
                factor = 1
            self.dx = self.speed*math.cos(angle)*factor
            self.dy = self.speed*math.sin(angle)*factor
            #print(self.dx, self.dy)

    def headToMate(self, other):
        self.foundMate = True
        xDist = other.cx - self.cx
        yDist = other.cy - self.cy
        #print("distances",xDist, yDist)
        if xDist == 0:
            if yDist > 0:
                self.dy = abs(self.speed)
            else:
                self.dy = abs(self.speed)*(-1)
            return
        angle = math.atan(yDist/xDist)
        if other.cx < self.cx:
            factor = -1
        else:
            factor = 1
        self.dx = self.speed*math.cos(angle)*factor
        self.dy = self.speed*math.sin(angle)*factor

    def consume(self, other, data):
        self.foundFood = False
        self.energy += 10
        #data.foodPieces.remove(other)

    def colorTraits(self):
        colorSpeed = str(hex(int((self.speed-1)*255)))[2:]
        colorSize = str(hex(int((self.size-1)*255)))[2:]
        colorSense = str(hex(int((self.sense-1)*255)))[2:]
        if len(colorSpeed) == 1:
            colorSpeed = "0" + colorSpeed
        if len(colorSize) == 1:
            colorSize = "0" + colorSize
        if len(colorSense) == 1:
            colorSense = "0" + colorSense
        #print(colorSpeed, colorSize, colorSense)
        resultColor = "#" + colorSpeed + colorSize + colorSense
        return resultColor

    def distance(self, x0, y0, x1, y1):
        return math.sqrt((x1-x0)**2+(y1-y0)**2)

    def sensing(self, data):
        # if self.foundMate == True:
        #     d = self.distance(self.mate.cx, self.mate.cy, self.cx, self.cy)
        #     if d > self.sense*40: #out of sight
        #         self.foundMate = False
        #         self.mate = None
        # if self.reproduceDelay <= 0 and self.foundMate == False: #heading to mate
        #     found = []
        #     for organism in data.organisms:
        #         d = self.distance(organism.cx, organism.cy, self.cx, self.cy)
        #         if  d <= self.sense*40 and isinstance(self, type(organism)):
        #             found.append((organism, d))
        #     closestD = math.inf
        #     closestOrganism = None
        #     for organism in found:
        #         if organism[1] < closestD:
        #             closestD = organism[1]
        #             closestOrganism = organism
        #     if closestOrganism != None:
        #         self.mate = closestOrganism[0]
        #         self.headToMate(closestOrganism[0])
        #         return
        if self.foundFood == False:
            found = []
            for food in data.foodPieces:
                d = self.distance(food.cx, food.cy, self.cx, self.cy)
                if  d <= self.sense*40:
                    found.append((food, d))
            closestD = math.inf
            closestFood = None
            for food in found:
                if food[1] < closestD:
                    closestD = food[1]
                    closestFood = food
            if closestFood != None:
                #print("heading to ",data.foodPieces.index(food[0]))
                self.headToFood(closestFood[0])


    def die(self, data):
        if self.energy <= 0:
            data.organisms.remove(self)
            return
        average = 0
        for organism in data.organisms:
            average += organism.energy
        average = average/len(data.organisms)
        if self.energy < average/2: #less then 25% percentile
            if random.randint(1, 500) <= data.percentDie: #die by chance
                data.organisms.remove(self)
                return
        if self.offsprings > self.maxReproduce:
            data.organisms.remove(self)

    def energyCost(self):
        #self.energy -= (1/2)*(self.size**3+self.sense)*self.speed**2
        self.energy -= self.size**self.sense*self.speed*(self.age/300+1)

    def onTimerFired(self, data):
        self.age += 1
        self.reproduceDelay -= 1
        self.fightDelay -= 1
        if self.age % 30 == 0 and self.age != 0:
            self.chanceDie += 1
        #self.die(data)
        if self.age % 10 == 0:
            self.energyCost()
        self.sensing(data)
        self.move(data)
        for food in data.foodPieces:
            #print(self.distance(food.cx, self.cx, food.cy, self.cy),food.r+self.size*10)
            if self.distance(food.cx, food.cy, self.cx, self.cy)<(food.r+self.size*10):
                self.consume(food, data)
                data.foodPieces.remove(food)
                #print(food in data.foodPieces)

    def reproduce(self, other, data):
        newSpeed = random.randint(int(min(self.speed*10, other.speed*10)), int(max(self.speed*10, other.speed*10)))/10
        newSize = random.randint(int(min(self.size*10, other.size*10)), int(max(self.size*10, other.size*10)))/10
        newSense = random.randint(int(min(self.sense*10, other.sense*10)), int(max(self.sense*10, other.sense*10)))/10
        if random.randint(0,100) <= data.mutateRate:
            temp = random.randint(-2,2)
            while (newSpeed + temp/10) < 1 or (newSpeed + temp/10) > 2:
                temp = random.randint(-2,2)
            newSpeed += temp/10
        if random.randint(0,100) <= data.mutateRate:
            temp = random.randint(-2,2)
            while (newSize + temp/10) < 1 or (newSize + temp/10) > 2:
                temp = random.randint(-2,2)
            newSize += temp/10
        if random.randint(0,100) <= data.mutateRate:
            temp = random.randint(-2,2)
            while (newSense + temp/10) < 1 or (newSense + temp/10) > 2:
                temp = random.randint(-2,2)
            newSense += temp/10
        self.offsprings += 1
        return newSpeed, newSize, newSense

    def isClicked(self, x, y):
        return self.cx-self.size*10<x<self.cx+self.size*10 and self.cy-self.size*10<y<self.cy+self.size*10


class SpeciesA(Organism):
    # def __init__(self, cx, cy, speed, size, sense): #!!!!
    #     # speed = random.randint(speedRange[0], speedRange[1])/10
    #     # size = random.randint(sizeRange[0], sizeRange[1])/10
    #     # sense = random.randint(senseRange[0], senseRange[1])/10
    #     super().__init__(cx, cy, speed, size, sense)
    def __init__(self, cx, cy, speed, size, sense, data, energy = 20, generation = 1):
        super().__init__(cx, cy, speed, size, sense, data, energy, generation)
        self.maxReproduce = data.maxReproduce[0]

    def reproduce(self, other, data):
        if self.age >= data.age and other.age >= data.age and self.reproduceDelay <= 0:
            if self.energy < 20:
                newEnergy = self.energy + 20
            else:
                newEnergy = 40
            newSpeed, newSize, newSense = super().reproduce(other, data)
            data.reproducedOrganisms.append(SpeciesA(self.cx, self.cy, newSpeed, newSize, newSense, data, newEnergy, self.generation+1))
            self.reproduceDelay = 50
            self.energy -= data.reproduceCost
            self.chanceDie *= 2
            self.foundMate = False
        elif self.reproduceDelay > 0:
            self.energyCost()



    def draw(self, canvas, x = None, y = None, drawSense = True):
        if x == None and y == None:
            x = self.cx
            y = self.cy
        color = self.colorTraits()
        if drawSense == True:
            canvas.create_oval(x-self.sense*40,y-self.sense*40, x+self.sense*40, y+self.sense*40)
        canvas.create_oval(x-self.size*10, y-self.size*10, x+self.size*10, y+self.size*10, fill=color)
        canvas.create_text(x, y, text = int(self.energy))


class SpeciesB(Organism):
    def __init__(self, cx, cy, speed, size, sense, data, energy = 20, generation = 1):
        super().__init__(cx, cy, speed, size, sense, data, energy, generation)
        self.maxReproduce = data.maxReproduce[1]

    def reproduce(self, other, data):
        if self.age >= data.age and other.age >= data.age and self.reproduceDelay <= 0:
            if self.energy < 20:
                newEnergy = self.energy + 20
            else:
                newEnergy = 40
            newSpeed, newSize, newSense = super().reproduce(other, data)
            data.reproducedOrganisms.append(SpeciesB(self.cx, self.cy, newSpeed, newSize, newSense, data, newEnergy, self.generation+1))
            self.reproduceDelay = 50
            self.energy -= data.reproduceCost
            self.chanceDie *= 2
            self.foundMate = False
        elif self.reproduceDelay > 0:
            self.energyCost()

    def draw(self, canvas, x = None, y = None, drawSense = True):
        if x == None and y == None:
            x = self.cx
            y = self.cy
        color = self.colorTraits()
        if drawSense == True:
            canvas.create_oval(x-self.sense*40, y-self.sense*40, x+self.sense*40, y+self.sense*40)
        canvas.create_rectangle(x-self.size*10, y-self.size*10, x+self.size*10, y+self.size*10, fill=color)
        canvas.create_text(x, y, text = int(self.energy))


class SpeciesC(Organism):
    def __init__(self, cx, cy, speed, size, sense, data, energy = 20, generation = 1):
        super().__init__(cx, cy, speed, size, sense, data, energy, generation)
        self.maxReproduce = data.maxReproduce[2]

    def reproduce(self, other, data):
        if self.age >= data.age and other.age >= data.age and self.reproduceDelay <= 0:
            if self.energy < 20:
                newEnergy = self.energy + 20
            else:
                newEnergy = 40
            newSpeed, newSize, newSense = super().reproduce(other, data)
            data.reproducedOrganisms.append(SpeciesC(self.cx, self.cy, newSpeed, newSize, newSense, data, newEnergy, self.generation+1))
            self.reproduceDelay = 50
            self.energy -= data.reproduceCost
            self.chanceDie *= 2
            self.foundMate = False
        elif self.reproduceDelay > 0:
            self.energyCost()

    def draw(self, canvas, x = None, y = None, drawSense = True):
        if x == None and y == None:
            x = self.cx
            y = self.cy
        color = self.colorTraits()
        if drawSense == True:
            canvas.create_oval(x-self.sense*40, y-self.sense*40, x+self.sense*40, y+self.sense*40)
        canvas.create_polygon(x, y-self.size*10, x+self.size*10, y+self.size*10, x-self.size*10, y+self.size*10, fill=color)
        canvas.create_text(x, y, text = int(self.energy))


class Food(object):
    def __init__(self, data, energy):
        self.cx = random.randint(0, data.width)
        self.cy = random.randint(0, data.height)
        self.r = 5
        self.timePassed = 0
        self.energy = energy

class Apple(Food):
    def __init__(self, data, energy = 7):
        super().__init__(data, energy)

    def draw(self, canvas, data):
        canvas.create_oval(self.cx-self.r, self.cy-self.r, self.cx+self.r, self.cy+self.r, fill="red")
        #canvas.create_text(self.cx, self.cy, text = str(data.foodPieces.index(self)))

class Banana(Food):
    def __init__(self, data, energy = 10):
        super().__init__(data, energy)

    def draw(self, canvas, data):
        canvas.create_oval(self.cx-self.r, self.cy-self.r, self.cx+self.r, self.cy+self.r, fill="yellow")
# Animation Starter Code, Focus on timerFired

from tkinter import *

#the template and run function taken from course notes
####################################
# customize these functions
####################################

def init(data, scene = None):
    # load data.xyz as appropriate
    data.organisms = []
    data.foodPieces = []
    data.maxReproduce = [2,2,2]
    data.traitPoints = [10,10,10]
    data.population = [20,20,20]
    data.speedRange = [(11,15),(11,15),(11,15)]
    data.sizeRange = [(11,15),(11,15),(11,15)]
    data.senseRange = [(11,15),(11,15),(11,15)]
    data.percentDie = 3
    data.timePassed = 0
    data.mutateRate = 10
    data.fightDelay = 2
    data.reproducedOrganisms = []
    data.foodFrequent = 30
    data.foodRange = (15,25)
    data.averageSpeed = 0
    data.averageSize = 0
    data.averageSense = 0
    data.age = 40
    data.reproduceCost = 10
    data.select = 0
    data.info = None
    data.scene = "Menu"
    data.tabSelect = "A"
    data.carnivore = [0,0,0]
    data.fieldSelect = 0
    data.generationCap = 20
    data.mode = None
    data.endSimulation = False
    data.endText = None
    data.showGraphs = False
    data.populationCount = [[],[],[]]
    data.traitCount = [[],[],[]]

def spawnOrganism(data):
    for i in range(data.population[0]):
        spawnA(data)
    for i in range(data.population[1]):
        spawnB(data)
    for i in range(data.population[2]):
        spawnC(data)
    # speed = random.randint(data.speedRange[0][0],data.speedRange[0][1])/10
    # size = random.randint(data.sizeRange[0][0],data.sizeRange[0][1])/10
    # sense = random.randint(data.senseRange[0][0],data.senseRange[0][1])/10
    # data.organisms.append(SpeciesA(400,400,speed, size, sense))

def spawnA(data, cx = None, cy = None):
    speed = random.randint(data.speedRange[0][0],data.speedRange[0][1])/10
    size = random.randint(data.sizeRange[0][0],data.sizeRange[0][1])/10
    sense = random.randint(data.senseRange[0][0],data.senseRange[0][1])/10
    if cx == None and cy == None:
        cx = random.randint(0, data.width)
        cy = random.randint(0, data.height)
    data.organisms.append(SpeciesA(cx, cy, speed, size, sense, data))

def spawnB(data, cx = None, cy = None):
    speed = random.randint(data.speedRange[1][0],data.speedRange[1][1])/10
    size = random.randint(data.sizeRange[1][0],data.sizeRange[1][1])/10
    sense = random.randint(data.senseRange[1][0],data.senseRange[1][1])/10
    if cx == None and cy == None:
        cx = random.randint(0, data.width)
        cy = random.randint(0, data.height)
    data.organisms.append(SpeciesB(cx, cy, speed, size, sense, data))

def spawnC(data, cx = None, cy = None):
    speed = random.randint(data.speedRange[2][0],data.speedRange[2][1])/10
    size = random.randint(data.sizeRange[2][0],data.sizeRange[2][1])/10
    sense = random.randint(data.senseRange[2][0],data.senseRange[2][1])/10
    if cx == None and cy == None:
        cx = random.randint(0, data.width)
        cy = random.randint(0, data.height)
    data.organisms.append(SpeciesC(cx, cy, speed, size, sense, data))


def mousePressed(event, data):
    # use event.x and event.y
    if data.scene == "Simulation":
        if data.info == None:
            for organism in data.organisms:
                if organism.isClicked(event.x, event.y):
                    data.info = organism
                    break
        else:
            if not data.info.isClicked(event.x, event.y):
                data.info = None
        if data.mode == "Simulation":
            buttonSize = 30
            margin = 5
            startX = data.width - buttonSize - margin
            buttonText = ["A", "B", "C"]
            endX = data.width - margin
            startY = margin
            if data.select == 0:
                for i in range(1,4):
                    endY = startY + buttonSize
                    if startX < event.x < endX and startY < event.y < endY:
                        data.select = i
                        break
                    startY += buttonSize
            elif data.select != 0:
                if data.select == 1:
                    spawnA(data, event.x, event.y)
                elif data.select == 2:
                    spawnB(data, event.x, event.y)
                elif data.select == 3:
                    spawnC(data, event.x, event.y)
                data.select = 0
    elif data.scene == "Menu":
        #check for click buttons
        if data.width/2-150<event.x<data.width/2+150:
            if data.height/2-50<event.y<data.height/2+50:
                data.scene = "Simulation Settings"
                data.mode = "Simulation"
            elif data.height*(2/3)-50<event.y<data.height*(2/3)+50:
                data.scene = "Competitive Settings"
                data.mode = "Competitive"
                data.foodFreqent = random.randint(3,8)*10
                foodRange = random.randint(3, 7)*5
                data.foodRange = (foodRange-5, foodRange+5)
                data.percentDie = random.randint(1,5)
                data.mutateRate = random.randint(5,15)
                data.fightDelay = random.randint(2,5)
                data.age = random.randint(2,5)*10
                data.generationCap = random.randint(3,6)*5
            elif data.height*(5/6)-50<event.y<data.height*(5/6)+50:
                data.scene = "Tutorial"
    elif data.scene == "Simulation Settings":
        if 0<event.y<100:
            if 0<event.x<data.width/3:
                data.tabSelect = "A"
            elif data.width/3<event.x<data.width*(2/3):
                data.tabSelect = "B"
            else:
                data.tabSelect = "C"
        else:
            if data.width*(3/4)-100<event.x<data.width*(3/4)+100:
                space = 0
                if data.height/6+space-20<event.y<data.height/6+space+20:
                    data.fieldSelect = 1
                space += 45
                if data.height/6+space-20<event.y<data.height/6+space+20:
                    data.fieldSelect = 2
                space += 45
                if data.height/6+space-20<event.y<data.height/6+space+20:
                    data.fieldSelect = 3
                space += 45
                if data.height/6+space-20<event.y<data.height/6+space+20:
                    data.fieldSelect = 4
                space += 45
                if data.height/6+space-20<event.y<data.height/6+space+20:
                    data.fieldSelect = 5
                space += 45
                if data.height/6+space-20<event.y<data.height/6+space+20:
                    data.fieldSelect = 6

                #global settings
                space = 80
                if data.height/2+space-20<event.y<data.height/2+space+20:
                    data.fieldSelect = 7
                space += 45
                if data.height/2+space-20<event.y<data.height/2+space+20:
                    data.fieldSelect = 8
                space += 45
                if data.height/2+space-20<event.y<data.height/2+space+20:
                    data.fieldSelect = 9
                space += 45
                if data.height/2+space-20<event.y<data.height/2+space+20:
                    data.fieldSelect = 10
                space += 45
                if data.height/2+space-20<event.y<data.height/2+space+20:
                    data.fieldSelect = 11
                space += 45
                if data.height/2+space-20<event.y<data.height/2+space+20:
                    data.fieldSelect = 12
                space += 45
                # if data.height/2+space-20<event.y<data.height/2+space+20:
                #     data.fieldSelect = 13
            if data.width/6-100<event.x<data.width/6+100 and data.height/2-120<event.y<data.height/2-50:
                if data.tabSelect == "C":
                    data.scene = "Simulation"
                    spawnOrganism(data)
                elif data.tabSelect == "A":
                    data.tabSelect = "B"
                elif data.tabSelect == "B":
                    data.tabSelect = "C"


    elif data.scene == "Competitive Settings":
        if 0<event.y<100:
            if 0<event.x<data.width/3:
                data.tabSelect = "A"
            elif data.width/3<event.x<data.width*(2/3):
                data.tabSelect = "B"
            else:
                data.tabSelect = "C"
        else:
            if data.width*(3/4)-100<event.x<data.width*(3/4)+100:
                space = 0
                if data.height/6+space-20<event.y<data.height/6+space+20:
                    data.fieldSelect = 1
                space += 45
                if data.height/6+space-20<event.y<data.height/6+space+20:
                    data.fieldSelect = 2
                space += 45
                if data.height/6+space-20<event.y<data.height/6+space+20:
                    data.fieldSelect = 3
                space += 45
                if data.height/6+space-20<event.y<data.height/6+space+20:
                    data.fieldSelect = 4
                space += 45
                if data.height/6+space-20<event.y<data.height/6+space+20:
                    data.fieldSelect = 5
                space += 45
                if data.height/6+space-20<event.y<data.height/6+space+20:
                    data.fieldSelect = 6
                #global settings are randomized
            #press play button
            if data.width/6-100<event.x<data.width/6+100 and data.height/2-120<event.y<data.height/2-50:
                if data.tabSelect == "C":
                    data.scene = "Simulation"
                    spawnOrganism(data)
                elif data.tabSelect == "A":
                    data.tabSelect = "B"
                elif data.tabSelect == "B":
                    data.tabSelect = "C"
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    if data.scene == "Simulation" and data.endSimulation == True:
        if event.keysym != None:
            init(data, "Menu")
    if data.scene == "Simulation":
        if event.keysym == "Escape":
            init(data)
    if (data.scene == "Simulation Settings" or data.scene == "Competitive Settings") and event.keysym == "Escape":
        init(data)
    if data.scene == "Tutorial" and event.keysym != None:
        init(data)
    if data.scene == "Simulation":
        # if event.keysym == "c":
        #     helper(data)
        if event.keysym == "Tab":
            if data.showGraphs == False:
                data.showGraphs = True
            else:
                data.showGraphs = False
    elif data.scene == "Simulation Settings":
        if data.tabSelect == "A":
            index = 0
        elif data.tabSelect == "B":
            index = 1
        else:
            index = 2
        if event.keysym == "Up":
            if data.fieldSelect == 1 and data.speedRange[index][1]<20:
                data.speedRange[index] = (data.speedRange[index][0]+1, data.speedRange[index][1]+1)
            if data.fieldSelect == 2 and data.sizeRange[index][1]<20:
                data.sizeRange[index] = (data.sizeRange[index][0]+1, data.sizeRange[index][1]+1)
            if data.fieldSelect == 3 and data.senseRange[index][1]<20:
                data.senseRange[index] = (data.senseRange[index][0]+1, data.senseRange[index][1]+1)
            if data.fieldSelect == 4:
                data.population[index] += 5
            if data.fieldSelect == 5:
                data.carnivore[index] = 1
            if data.fieldSelect == 6:
                data.maxReproduce[index] += 1
            if data.fieldSelect == 7:
                data.foodFrequent += 10
            if data.fieldSelect == 8:
                data.foodRange = (data.foodRange[0]+5, data.foodRange[1]+5)
            if data.fieldSelect == 9 and data.percentDie < 100:
                data.percentDie += 1
            if data.fieldSelect == 10 and data.mutateRate < 100:
                data.mutateRate += 1
            if data.fieldSelect == 11:
                data.fightDelay += 1
            if data.fieldSelect == 12:
                data.age += 10
            # if data.fieldSelect == 13:
            #     data.generationCap += 1
        elif event.keysym == "Down":
            if data.fieldSelect == 1 and data.speedRange[index][0]>11:
                data.speedRange[index] = (data.speedRange[index][0]-1, data.speedRange[index][1]-1)
            if data.fieldSelect == 2 and data.sizeRange[index][0]>11:
                data.sizeRange[index] = (data.sizeRange[index][0]-1, data.sizeRange[index][1]-1)
            if data.fieldSelect == 3 and data.senseRange[index][0]>1:
                data.senseRange[index] = (data.senseRange[index][0]-1, data.senseRange[index][1]-1)
            if data.fieldSelect == 4 and data.population[index]>0:
                data.population[index] -= 5
            if data.fieldSelect == 5:
                data.carnivore[index] = 0
            if data.fieldSelect == 6:
                data.maxReproduce[index] -= 1
            if data.fieldSelect == 7 and data.foodFrequent > 10:
                data.foodFrequent -= 10
            if data.fieldSelect == 8 and data.foodRange[0]>5 and data.foodRange[1]>5:
                data.foodRange = (data.foodRange[0]-5, data.foodRange[1]-5)
            if data.fieldSelect == 9 and data.percentDie > 0:
                data.percentDie -= 1
            if data.fieldSelect == 10 and data.mutateRate > 0:
                data.mutateRate -= 1
            if data.fieldSelect == 11 and data.fightDelay > 1:
                data.fightDelay -= 1
            if data.fieldSelect == 12 and data.age > 10:
                data.age -= 10
            # if data.fieldSelect == 13 and data.generationCap > 2:
            #     data.generationCap -= 1

    elif data.scene == "Competitive Settings":
        if data.tabSelect == "A":
            index = 0
        elif data.tabSelect == "B":
            index = 1
        else:
            index = 2
        if event.keysym == "Up":
            if data.fieldSelect == 1 and data.speedRange[index][1]<20 and data.traitPoints[index]>0:
                data.speedRange[index] = (data.speedRange[index][0]+1, data.speedRange[index][1]+1)
                data.traitPoints[index] -= 1
            if data.fieldSelect == 2 and data.sizeRange[index][1]<20 and data.traitPoints[index]>0:
                data.sizeRange[index] = (data.sizeRange[index][0]+1, data.sizeRange[index][1]+1)
                data.traitPoints[index] -= 1
            if data.fieldSelect == 3 and data.senseRange[index][1]<20 and data.traitPoints[index]>0:
                data.senseRange[index] = (data.senseRange[index][0]+1, data.senseRange[index][1]+1)
                data.traitPoints[index] -= 1
            if data.fieldSelect == 4 and data.traitPoints[index]>0:
                data.population[index] += 5
                data.traitPoints[index] -= 1
            if data.fieldSelect == 5 and data.traitPoints[index]>0:
                data.carnivore[index] = 1
                data.traitPoints[index] -= 1
            if data.fieldSelect == 6 and data.traitPoints[index]>0:
                data.maxReproduce[index] += 1
                data.traitPoints[index] -= 1
        elif event.keysym == "Down":
            if data.fieldSelect == 1 and data.speedRange[index][0]>11:
                data.speedRange[index] = (data.speedRange[index][0]-1, data.speedRange[index][1]-1)
                data.traitPoints[index] += 1
            if data.fieldSelect == 2 and data.sizeRange[index][0]>11:
                data.sizeRange[index] = (data.sizeRange[index][0]-1, data.sizeRange[index][1]-1)
                data.traitPoints[index] += 1
            if data.fieldSelect == 3 and data.senseRange[index][0]>11:
                data.senseRange[index] = (data.senseRange[index][0]-1, data.senseRange[index][1]-1)
                data.traitPoints[index] += 1
            if data.fieldSelect == 4 and data.population[index]>0:
                data.population[index] -= 5
                data.traitPoints[index] += 1
            if data.fieldSelect == 5:
                data.carnivore[index] = 0
                data.traitPoints[index] += 1
            if data.fieldSelect == 6:
                data.maxReproduce[index] -= 1
                data.traitPoints[index] += 1

    pass

    # for j in range(len(data.organisms)):
    #     check = data.organisms[i].distance(data.organisms[i].cx, data.organisms[i].cy, data.organisms[j].cx, data.organisms[j].cy)<(data.organisms[i].size*10+data.organisms[j].size*10)
    #     if check and i!=j:
    #         if isinstance(data.organisms[i], type(data.organisms[j])):
    #             print(data.organisms[i].cx, data.organisms[i].cy, data.organisms[j].cx, data.organisms[j].cy)
    #             #print(type(organism), type(other))
    #             data.organisms[i].reproduce(data.organisms[j], data)
def fight(organism, other, data):
    chance = (organism.size/other.size)*100-50
    if random.randint(1, 100) <= chance and organism.fightDelay <= 0:
        #print(other.energy, other.energy-(organism.size/other.size)*3)
        temp = (organism.size/other.size)*3
        other.energy -= temp
        if isinstance(organism, SpeciesA) and data.carnivore[0] == 1:
            organism.energy += temp
        elif isinstance(organism, SpeciesB) and data.carnivore[1] == 1:
            organism.enery += temp
        elif isinstance(organism, SpeciesC) and data.carnivore[2] == 1:
            organism.energy += temp
        organism.fightDelay = data.fightDelay
    elif other.fightDelay <= 0:
        temp = (other.size/organism.size)*3
        organism.energy -= temp
        if isinstance(other, SpeciesA) and data.carnivore[0] == 1:
            other.energy += temp
        elif isinstance(other, SpeciesB) and data.carnivore[1] == 1:
            other.energy += temp
        elif isinstance(organism, SpeciesC) and data.carnivore[2] == 1:
            other.energy += temp
        other.fightDelay = data.fightDelay

def helper(data):
    #print(len(data.organisms), end =" ")
    if data.endSimulation == False:
        if data.timePassed % data.foodFrequent == 0:
            numFood = random.randint(data.foodRange[0], data.foodRange[1])
            for i in range(numFood):
                data.foodPieces.append(Apple(data))
            numFood = random.randint(data.foodRange[0], data.foodRange[1])
            for i in range(numFood):
                data.foodPieces.append(Banana(data))

        for food in data.foodPieces:
            food.timePassed += 1
            if food.timePassed >= 100:
                data.foodPieces.remove(food)
        for organism in data.organisms: #remember to sync with the commented code below
            organism.onTimerFired(data)
            # for j in range(len(data.organisms)):
            #     check = data.organisms[i].distance(data.organisms[i].cx, data.organisms[i].cy, data.organisms[j].cx, data.organisms[j].cy)<(data.organisms[i].size*10+data.organisms[j].size*10)
            #     if check and i!=j:
            #         if isinstance(data.organisms[i], type(data.organisms[j])):
            #             print(data.organisms[i].cx, data.organisms[i].cy, data.organisms[j].cx, data.organisms[j].cy)
            #             #print(type(organism), type(other))
            #             data.organisms[i].reproduce(data.organisms[j], data)
            for other in data.organisms:
                check = organism.distance(organism.cx, organism.cy, other.cx, other.cy)<(organism.size*10+other.size*10)
                check1 = organism is other
                if check and check1 == False:
                    if isinstance(organism, type(other)):
                        organism.reproduce(other, data)
                    elif random.randint(1,100) <= 5: #chance of cross-breeding
                        organism.reproduce(other, data)
                        other.reproduce(organism, data)
                    else: #fight
                        fight(organism, other, data)
            organism.die(data)
        #print(len(data.organisms),end=" ")
        data.organisms.extend(data.reproducedOrganisms)
        #print(len(data.organisms))
        data.reproducedOrganisms = []
        #print(data.timePassed)
        # if len(data.organisms) == 1:
        #     print(data.organisms[0].speed, data.organisms[0].size, data.organisms[0].sense, data.organisms[0].energy)
        data.averageSpeed = 0
        data.averageSize = 0
        data.averageSense = 0
        for organism in data.organisms:
            data.averageSpeed += organism.speed
            data.averageSize += organism.size
            data.averageSense += organism.sense
        data.averageSpeed /= len(data.organisms)
        data.averageSize /= len(data.organisms)
        data.averageSense /= len(data.organisms)
        #print("Average Speed: ", data.averageSpeed, "Average Size: ", data.averageSize, "Average Sense: ", data.averageSense)
        if data.info != None and data.info not in data.organisms:
            data.info = None
        if data.mode == "Competitive" and (countGeneration(data) >= data.generationCap or len(data.organisms) == 1):
            data.endSimulation = True
    data.timePassed += 1
    #pass

def timerFired(data):
    # if data.timePassed % 30 == 0:
    #     for i in range(30):
    #         data.foodPieces.append(Food(data))
    # for food in data.foodPieces:
    #     food.timePassed += 1
    #     if food.timePassed >= 100:
    #         data.foodPieces.remove(food)
    # for organism in data.organisms:
    #     organism.onTimerFired(data)
    #     for other in data.organisms:
    #         check = organism.distance(organism.cx, organism.cy, other.cx, other.cy)<(organism.size*10+other.size*10)
    #         check1 = organism is other
    #         if check and check1 == False:
    #             if isinstance(organism, type(other)):
    #                 print(type(organism), type(other))
    #                 organism.reproduce(other, data)
    # print(data.timePassed)
    # if len(data.organisms) == 1:
    #     print(data.organisms[0].speed, data.organisms[0].size, data.organisms[0].sense)
    # data.timePassed += 1\
    if data.scene == "Simulation":
        helper(data)
        if data.timePassed % 10 == 0:
            popCount = [0,0,0]
            trait = [0,0,0]
            for organism in data.organisms:
                if isinstance(organism, SpeciesA):
                    popCount[0] += 1
                elif isinstance(organism, SpeciesB):
                    popCount[1] += 1
                else:
                    popCount[2] += 1
                trait[0] += organism.speed
                trait[1] += organism.size
                trait[2] += organism.sense
            for i in range(3):
                trait[i] /= len(data.organisms)
            for i in range(3):
                data.populationCount[i].append(popCount[i]) #add data points
                data.traitCount[i].append(trait[i])
    pass

def drawSpawnButton(canvas, data):
    buttonSize = 30
    margin = 5
    startX = data.width - buttonSize - margin
    buttonText = ["A", "B", "C"]
    endX = data.width - margin
    startY = margin
    for i in range(1,4):
        endY = startY + buttonSize
        canvas.create_rectangle(startX, startY, endX, endY, fill = "white")
        x = (startX+endX)/2
        y = (startY+endY)/2
        canvas.create_text(x,y,text = buttonText[i-1])
        startY += buttonSize


def countGeneration(data):
    generation = 0
    for organism in data.organisms:
        if organism.generation > generation:
            generation = organism.generation
    return generation

def showInfo(data, canvas):
    frameSize = 150
    buttonSize = 30
    margin = 5
    canvas.create_rectangle(data.width-buttonSize-2*margin-frameSize, margin, data.width-buttonSize-2*margin, frameSize+margin, fill = "white")
    data.info.draw(canvas, data.width-buttonSize-2*margin-frameSize/2, frameSize/4+margin, False)
    speedTxt = "Speed: " + str((data.info.speed))
    sizeTxt = "Size: " + str((data.info.size))
    senseTxt = "Sense: " + str((data.info.sense))
    canvas.create_text(data.width-buttonSize-2*margin-frameSize/2, frameSize*(5/8)+margin, text = speedTxt )
    canvas.create_text(data.width-buttonSize-2*margin-frameSize/2, frameSize*(6/8)+margin, text = sizeTxt )
    canvas.create_text(data.width-buttonSize-2*margin-frameSize/2, frameSize*(7/8)+margin, text = senseTxt )

def drawSimulation(canvas, data):
    for organism in data.organisms:
        organism.draw(canvas)
    for food in data.foodPieces:
        food.draw(canvas, data)
    generation = "Generation: " + str(countGeneration(data))
    canvas.create_text(data.width/15, data.height/23, text = generation, font = "Chalkboard 15 bold")
    if data.mode == "Simulation":
        drawSpawnButton(canvas, data)
    if data.info != None:
        showInfo(data, canvas)

def drawMenu(canvas, data):
    buttonSize = 150
    canvas.create_text(data.width/2, data.height/4, text = "Evolution+", font = "Chalkboard 80 bold")
    canvas.create_rectangle(data.width/2-buttonSize, data.height/2-buttonSize/3, data.width/2+buttonSize, data.height/2+buttonSize/3, fill = "orange")
    canvas.create_text(data.width/2, data.height/2, text = "Simulation Mode", font = "Chalkboard 30 bold")
    canvas.create_rectangle(data.width/2-buttonSize, data.height*(2/3)-buttonSize/3, data.width/2+buttonSize, data.height*(2/3)+buttonSize/3, fill = "orange")
    canvas.create_text(data.width/2, data.height*(2/3), text = "Competitve Mode", font = "Chalkboard 30 bold")
    canvas.create_rectangle(data.width/2-buttonSize, data.height*(5/6)-buttonSize/3, data.width/2+buttonSize, data.height*(5/6)+buttonSize/3, fill = "orange")
    canvas.create_text(data.width/2, data.height*(5/6), text = "Tutorial", font = "Chalkboard 30 bold")

def drawTabs(canvas, data):
    species = ["Species A", "Species B", "Species C"]
    for i in range(3):
        x0 = i*data.width/3
        y0 = 0
        x1 = (i+1)*data.width/3
        y1 = 100
        color = "white"
        if data.tabSelect == species[i][8:]:
            color = "#FF7F50"
        canvas.create_rectangle(x0,y0,x1,y1, fill = color)
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text = species[i], font = "Chalkboard 20 bold")


def findAverage(x):
    return (x[0]+x[1])/2


def drawSimulationSettings(canvas, data):
    drawTabs(canvas, data)
    if data.tabSelect == "A":
        species = SpeciesA(data.width/4, data.height/4, findAverage(data.speedRange[0])/10, findAverage(data.sizeRange[0])/10, findAverage(data.senseRange[0])/10, data)
        index = 0
    elif data.tabSelect == "B":
        species = SpeciesB(data.width/4, data.height/4, findAverage(data.speedRange[1])/10, findAverage(data.sizeRange[1])/10, findAverage(data.senseRange[1])/10, data)
        index = 1
    else:
        species = SpeciesC(data.width/4, data.height/4, findAverage(data.speedRange[2])/10, findAverage(data.sizeRange[2])/10, findAverage(data.senseRange[2])/10, data)
        index = 2

    species.draw(canvas, data.width/6, data.height/4, False) #draw visual image


    space = 0
    color = "black"
    if data.fieldSelect == 1:
        color = "orange"
    canvas.create_text(data.width/2, data.height/6, text = "Average Speed:", font = "Chalkboard 20 bold")
    canvas.create_rectangle(data.width*(3/4)-100, data.height/6-20, data.width*(3/4)+100, data.height/6+20, outline = color)
    canvas.create_text(data.width*(3/4), data.height/6+space, text = species.speed)


    space += 45
    color = "black"
    if data.fieldSelect == 2:
        color = "orange"
    canvas.create_text(data.width/2, data.height/6+space, text = "Average Size:", font = "Chalkboard 20 bold")
    canvas.create_rectangle(data.width*(3/4)-100, data.height/6+space-20, data.width*(3/4)+100, data.height/6+space+20, outline = color)
    canvas.create_text(data.width*(3/4), data.height/6+space, text = species.size)



    space += 45
    color = "black"
    if data.fieldSelect == 3:
        color = "orange"
    canvas.create_text(data.width/2, data.height/6+space, text = "Average Sense:", font = "Chalkboard 20 bold")
    canvas.create_rectangle(data.width*(3/4)-100, data.height/6+space-20, data.width*(3/4)+100, data.height/6+space+20, outline = color)
    canvas.create_text(data.width*(3/4), data.height/6+space, text = species.sense)




    space += 45
    color = "black"
    if data.fieldSelect == 4:
        color = "orange"
    canvas.create_text(data.width/2, data.height/6+space, text = "Population:", font = "Chalkboard 20 bold")
    canvas.create_rectangle(data.width*(3/4)-100, data.height/6+space-20, data.width*(3/4)+100, data.height/6+space+20, outline = color)
    canvas.create_text(data.width*(3/4), data.height/6+space, text = data.population[index])



    space += 45
    color = "black"
    if data.fieldSelect == 5:
        color = "orange"
    canvas.create_text(data.width/2, data.height/6+space, text = "Carnivore:", font = "Chalkboard 20 bold")
    canvas.create_rectangle(data.width*(3/4)-100, data.height/6+space-20, data.width*(3/4)+100, data.height/6+space+20, outline = color)
    canvas.create_text(data.width*(3/4), data.height/6+space, text = data.carnivore[index])



    space += 45
    color = "black"
    if data.fieldSelect == 6:
        color = "orange"
    canvas.create_text(data.width/2, data.height/6+space, text = "Max Offsprings:", font = "Chalkboard 20 bold")
    canvas.create_rectangle(data.width*(3/4)-100, data.height/6+space-20, data.width*(3/4)+100, data.height/6+space+20, outline = color)
    canvas.create_text(data.width*(3/4), data.height/6+space, text = species.maxReproduce)



    #global settings
    canvas.create_rectangle(0, data.height/2, data.width, data.height)
    canvas.create_text(data.width/2, data.height/2+30, text = "Global Settings", font = "Chalkboard 30 bold")


    space = 80
    color = "black"
    if data.fieldSelect == 7:
        color = "orange"
    canvas.create_text(data.width/4, data.height/2+space, text = "Food Frequency:", font = "Chalkboard 20 bold")
    canvas.create_rectangle(data.width*(3/4)-100, data.height/2+space-20, data.width*(3/4)+100, data.height/2+space+20, outline = color)
    canvas.create_text(data.width*(3/4), data.height/2+space, text = int(data.foodFrequent/10))



    space += 45
    color = "black"
    if data.fieldSelect == 8:
        color = "orange"
    canvas.create_text(data.width/4, data.height/2+space, text = "Average Food:", font = "Chalkboard 20 bold")
    canvas.create_rectangle(data.width*(3/4)-100, data.height/2+space-20, data.width*(3/4)+100, data.height/2+space+20, outline = color)
    canvas.create_text(data.width*(3/4), data.height/2+space, text = int(findAverage(data.foodRange)))


    space += 45
    color = "black"
    if data.fieldSelect == 9:
        color = "orange"
    canvas.create_text(data.width/4, data.height/2+space, text = "Chance of Heart Attack:", font = "Chalkboard 20 bold")
    canvas.create_rectangle(data.width*(3/4)-100, data.height/2+space-20, data.width*(3/4)+100, data.height/2+space+20, outline = color)
    canvas.create_text(data.width*(3/4), data.height/2+space, text = data.percentDie)



    space += 45
    color = "black"
    if data.fieldSelect == 10:
        color = "orange"
    canvas.create_text(data.width/4, data.height/2+space, text = "Mutate Rate:", font = "Chalkboard 20 bold")
    canvas.create_rectangle(data.width*(3/4)-100, data.height/2+space-20, data.width*(3/4)+100, data.height/2+space+20, outline = color)
    canvas.create_text(data.width*(3/4), data.height/2+space, text = data.mutateRate)



    space += 45
    color = "black"
    if data.fieldSelect == 11:
        color = "orange"
    canvas.create_text(data.width/4, data.height/2+space, text = "Fight Delay:", font = "Chalkboard 20 bold")
    canvas.create_rectangle(data.width*(3/4)-100, data.height/2+space-20, data.width*(3/4)+100, data.height/2+space+20, outline = color)
    canvas.create_text(data.width*(3/4), data.height/2+space, text = data.fightDelay/10)



    space += 45
    color = "black"
    if data.fieldSelect == 12:
        color = "orange"
    canvas.create_text(data.width/4, data.height/2+space, text = "Reproductive Age:", font = "Chalkboard 20 bold")
    canvas.create_rectangle(data.width*(3/4)-100, data.height/2+space-20, data.width*(3/4)+100, data.height/2+space+20, outline = color)
    canvas.create_text(data.width*(3/4), data.height/2+space, text = int(data.age)/10)


    if data.scene == "Competitive Settings":
        space += 45
        color = "black"
        if data.fieldSelect == 13:
            color = "orange"
        canvas.create_text(data.width/4, data.height/2+space, text = "Generation Cap:", font = "Chalkboard 20 bold")
        canvas.create_rectangle(data.width*(3/4)-100, data.height/2+space-20, data.width*(3/4)+100, data.height/2+space+20, outline = color)
        canvas.create_text(data.width*(3/4), data.height/2+space, text = data.generationCap)

    canvas.create_rectangle(data.width/6-100, data.height/2-120, data.width/6+100, data.height/2-50, fill = "light green")
    if data.tabSelect == "C":
        txt = "Start"
    else:
        txt = "Ready"
    canvas.create_text(data.width/6, data.height/2-85, text = txt, fill = "magenta", font = "Chalkboard 20 bold")

def drawCompetitiveSettings(canvas, data):
    drawSimulationSettings(canvas, data)
    for i in range(0,3):
        x = (data.width/3*i+data.width/3*(i+1))/2
        y = 75
        txt = "Trait Points Left: " + str(data.traitPoints[i])
        canvas.create_text(x, y, text = txt)

def drawEnd(canvas, data):
    canvas.create_rectangle(data.width/2-270, data.height/2-270, data.width/2+270, data.height/2+270, fill = "#FFA500")
    count = [0,0,0]
    for organism in data.organisms:
        if isinstance(organism, SpeciesA):
            count[0] += 1
        elif isinstance(organism, SpeciesB):
            count[1] += 1
        elif isinstance(organism, SpeciesC):
            count[2] += 1
    highestCount = count.index(max(count))
    txt1 = "Species "
    if data.endText == None:
        data.endText = "has won the genetics"
    if highestCount == 0:
        txt2 = "A "
    elif highestCount == 1:
        txt2 = "B "
    elif highestCount == 2:
        txt2 = "C "
    canvas.create_text(data.width/2, data.height/2-100, text = txt1+txt2+data.endText, font = "Chalkboard 35 bold", fill = "black" )
    canvas.create_text(data.width/2, data.height/2-50, text = "lottery!", font = "Chalkboard 35 bold" ,fill = "black")
    canvas.create_text(data.width/2, data.height/2+50, text = "Press any key to return to main menu", font = "Chalkboard 25 bold", fill = "black")

def drawTutorial(canvas, data):
    canvas.create_text(data.width/2, 50, text = "Evolution+ Tutorial", font = "Chalkboard 40 bold")
    canvas.create_text(data.width/2, data.height/2+30, text = "-Evolution+ is a simulation game in which you can simulate the process of\nnatural selection based of customized organisms and species.\n\n-Each organism has 3 basic traits of speed, size, and sense, which are represented\nby shades of red, green, and blue, respectively.\n\n-There are also global settings which is shared for a particular session of\nsimulation,including frequency of food (in seconds), average food count, chance\nof dying because of heart attack, mutate rate, fighting delay (in seconds), and\nreproductive age.\n\n-The goal of the simulation is to find the right combination of traits for the species\nof your choice to thrive in a particular environment.\n\n-There are two modes, which are Simulation Mode and Competitive Mode. In\nSimulation Mode, you are allowed to change any simulation settings, including\nspecies-specific as well as global settings, to investigate any combination of\ntraits yourself. In Competitive Mode, up to 3 players are allowed to compete with\neach other, in which each player customize their chosen species so that its\ncombination of traits outperform other players' species. However, players in\nCompetitive Mode are only allowed to have 10 Trait Points to upgrade their species'\ntraits each round, and global settings will be randomized.\n\n-During each simulation, you can press TAB to view graphs that show statistics of\nthe simulation. Finally, if you are in Simulation-only Mode, you can intervene by\nplacing new organisms into the environment.\n\n-Now that you have learned the basics, press any key to return to main menu and\nstart evolving!", font = "Chalkboard 18 bold")

def drawPopulation(canvas, data, x, y, r):
    canvas.create_rectangle(x-r, y-r, x+r, y+r, fill = "white")
    canvas.create_text(x, y-r+20, text = "Population by Species", font = "Chalkboard 20 bold")
    canvas.create_text(x, y-r+50, text = "A = Red, B = Green, C = Blue", font = "Chalkboard 15 bold")
    lineColor = ["red", "green", "blue"]
    index = 0
    for species in data.populationCount:
        x0 = x-r
        y0 = y+r
        time = 10
        for point in species:
            y1 = (y+r)-(point/len(data.organisms))*2*r
            x1 = (x-r)+(time/data.timePassed)*2*r
            canvas.create_line(x0,y0,x1,y1, fill = lineColor[index])
            time += 10
            x0 = x1
            y0 = y1
            #print(x0,x1,y0,y1)
        index += 1
    # for count in data.populationCount:
    #     if count[len(count)-1] == 0:
    #         data.endSimulation = True

def drawTraits(canvas, data, x, y, r):
    canvas.create_rectangle(x-r, y-r, x+r, y+r, fill = "white")
    canvas.create_text(x, y-r+20, text = "Average Traits", font = "Chalkboard 20 bold")
    canvas.create_text(x, y-r+50, text = "Speed = Red, Size = Green, Sense = Blue", font = "Chalkboard 15 bold")
    lineColor = ["red", "green", "blue"]
    index = 0
    for species in data.traitCount:
        x0 = x-r
        y0 = y+r
        time = 10
        for point in species:
            y1 = (y+r)-(point-1)*2*r
            x1 = (x-r)+(time/data.timePassed)*2*r
            canvas.create_line(x0,y0,x1,y1, fill = lineColor[index])
            time += 10
            x0 = x1
            y0 = y1
            #print(x0,x1,y0,y1)
        index += 1

def drawGraphs(canvas, data):
    drawPopulation(canvas, data, data.width/4, data.height/2, 175)
    drawTraits(canvas, data, data.width*(3/4), data.height/2, 175)

def redrawAll(canvas, data):
    # draw in canvas
    if data.scene == "Simulation":
        drawSimulation(canvas, data)
        if data.showGraphs == True:
            drawGraphs(canvas, data)
        if data.endSimulation == True:
            drawEnd(canvas, data)
    elif data.scene == "Menu":
        drawMenu(canvas, data)
    elif data.scene == "Simulation Settings":
        drawSimulationSettings(canvas, data)
    elif data.scene == "Competitive Settings":
        drawCompetitiveSettings(canvas, data)
    elif data.scene == "Tutorial":
        drawTutorial(canvas, data)
    pass

#taken from https://www.cs.cmu.edu/~112-n19/notes/notes-animations-part2.html
####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 50 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(800, 800)