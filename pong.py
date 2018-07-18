#idle 3.6.4
import pygame
import pygame_setup as pg
import random, time

white = (255,255,255)
black = (0,0,0)

class Vector():
    def __init__(self):
        self.x = 0
        self.y = 0

    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def setX(self,newX):
        self.x = newX
    def setY(self,newY):
        self.y = newY

class Paddle():
    def __init__(self,x,y):
        self.width = 10
        self.height = 50
        self.x = x
        self.y = y
        self.speed = 10
        self.score = 0
        self.originalx = self.x
        self.originaly = self.y
        
    def getImage(self):
        return pygame.draw.rect(app.getScreen(),white,(self.x,self.y,self.width,self.height))
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def setX(self,newX):
        self.x = newX
    def setY(self,newY):
        if newY+self.height < app.getHeight() and newY > 0:
            self.y = newY
    def getSpeed(self):
        return self.speed
    def getScore(self):
        return self.score
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height
    def increaseScore(self):
        self.score+=1
    def reset(self):
        self.x = self.originalx
        self.y = self.originaly

class Puck(Paddle):
    def __init__(self,x,y):
        Paddle.__init__(self,x,y)
        self.width = 10
        self.height = 10
        self.velocity = Vector()
        self.setRandomVelocity()

    def update(self):
        newx = self.x + (self.velocity.getX()*app.getClock().get_time())
        newy = self.y + (self.velocity.getY()*app.getClock().get_time())

        pygame.display.update()
        if p1.getImage().collidepoint(newx+p1.getWidth()//2,newy):
            self.velocity.setX(self.velocity.getX()*-1)
            dy = getNewY(p1)
            self.velocity.setY(dy*0.01)
        elif p2.getImage().collidepoint(newx+p1.getWidth()//2,newy):
            self.velocity.setX(self.velocity.getX()*-1)
            dy = getNewY(p2)
            self.velocity.setY(dy*0.01)

        elif newx < 0:
            p2.increaseScore()
            reset()
        elif newx > app.getWidth():
            p1.increaseScore()
            reset()

        else:
            self.x = newx

        if newy >= 0 and newy <= app.getHeight()-self.height:
            self.y = newy
        else:
            self.velocity.setY(self.velocity.getY()*-1)

    def setRandomVelocity(self):
        x = 0
        y = 0
        while x == 0 and y == 0:
            x1 = random.uniform(0.2,0.3)
            x2 = random.uniform(-0.2,-0.3)
            x = random.choice([x1,x2])
            y = random.uniform(-0.1,0.1)
        self.velocity.setX(x)
        self.velocity.setY(y)

#______________________________________

def getNewY(paddle):
    pucky = puck.getY()
    paddley = paddle.getY()
    midpaddle = paddle.getHeight()//2
    midpaddle = paddley + midpaddle
    difference = pucky - midpaddle
    if puck.velocity.getY() > 0:
        return abs(difference)
    else:
        if difference > 0:
            difference *= -1
        return difference

def reset():
    p1.reset()
    p2.reset()
    puck.reset()
    puck.setRandomVelocity()
    render()
    time.sleep(0.5)
    
def render():
    app.getScreen().fill(black)
    pg.renderText(str(p1.getScore()),30,white,(app.getWidth()//2)-37,30,app.getScreen())
    pg.renderText(str(p2.getScore()),30,white,(app.getWidth()//2)+15,30,app.getScreen())
    pygame.draw.line(app.getScreen(),white,(app.getWidth()//2,0),(app.getWidth()//2,app.getHeight()))
    p1.getImage()
    p2.getImage()
    puck.getImage()
    pygame.display.update()
    app.Tick()

def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            app.exit()
        elif event.type == pygame.KEYDOWN:
            if pg.getKey(event.key) == "s":
                pg.saveImage(app.getScreen())

    keys=pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        p2.setY(p2.getY()-p2.getSpeed())
    if keys[pygame.K_DOWN]:
        p2.setY(p2.getY()+p2.getSpeed())
    if keys[pygame.K_e]:
        p1.setY(p1.getY()-p1.getSpeed())
    if keys[pygame.K_d]:
        p1.setY(p1.getY()+p1.getSpeed())
    
def main():
    gameOver = False
    app.begin()
    while not gameOver:
        render()
        events()
        puck.update()

if __name__ == "__main__":
    app = pg.App(600,400,32,'Pong')
    p1 = Paddle(30,app.getHeight()//2)
    p2 = Paddle(app.getWidth()-30,app.getHeight()//2)
    puck = Puck(app.getWidth()//2,app.getHeight()//2)
    main()
    
