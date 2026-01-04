import pygame as pg
import math as m
import random as r

pg.init()

HEIGHT = 700
WIDTH = 600

bakgrunn = pg.image.load("flappy/bakgrunn.png")
bakgrunn = pg.transform.scale(bakgrunn, (WIDTH, HEIGHT))

fugl = pg.image.load("flappy/bird.png")

clock = pg.time.Clock()

class App:
    def __init__(self,height = HEIGHT, width = WIDTH, score = 0):
        self.height = height
        self.width = width
        self.score = score
    
    def setup(self):
        self.vindu = pg.display.set_mode((self.width,self.height))
        self.bird = Bird(self.width//2,self.height//2,0)

        self.hindring1 = Hindring(WIDTH)
        self.hindring2 = Hindring(WIDTH*1.5)

    def render(self):
        self.vindu.fill((255,255,255))
        self.vindu.blit(bakgrunn,(0,0))

        self.bird.render(self.vindu)

        self.hindring1.render(self.vindu)
        self.hindring2.render(self.vindu)

        if self.bird.G == 0:
            font = pg.font.SysFont(None,17)
            text = font.render(f'Trykk på mellomrom / SPACE', True, (0, 0, 0))        
            self.vindu.blit(text, (self.width // 2 -75 , self.height // 2+50))

        pg.display.set_caption(str(self.score))
        pg.display.flip()
    
    def run(self):
        self.setup()
        self.running = True

        while self.running:

            self.bird.gravitasjon()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.bird.beveg()

            self.render()

            # Score skal ikke påvirkes før spillet er i gang, og G ikke er lik 0
            if self.bird.G != 0: 
                self.hindring1.beveg()
                self.hindring2.beveg()

                #beveger blokkene først, slik at logikken nedenfor skal fungere som ønsket selv for den første blokken, som jo begynner med x = bredde

                if self.hindring2.x == WIDTH:
                    self.score +=1
                elif self.hindring1.x == WIDTH:
                    self.score +=1

            #kollisjonssjekk
            #hindring 1
            if self.bird.x in range(int(self.hindring1.x-self.bird.r) , int(self.hindring1.x+self.hindring1.width+self.bird.r)): #dersom fuglen, med noe ekstra margin, er ved en hindring (x)
                if self.bird.y+self.bird.r >= self.hindring1.y+self.hindring1.diff: #dersom fuglens y (pluss radius) er "større" enn det hindringens y er, altså kollisjon på nedre del
                    self.running = False
                    break

                elif self.bird.y-self.bird.r <= self.hindring1.y:   #derson fuglens y, minus radius, (fuglens ytre kant) er "mindre" enn (fuglen er høyere opp enn) hindringens topp
                    self.running = False                            #dette vil dermed også fungere for kollisjoner med sideveggene
                    break

            #hindring 2, samme logikk som over
            if self.bird.x in range(int(self.hindring2.x-self.bird.r) , int(self.hindring2.x+self.hindring2.width+self.bird.r)):
                if self.bird.y+self.bird.r >= self.hindring2.y+self.hindring2.diff:
                    self.running = False
                    break

                elif self.bird.y-self.bird.r <= self.hindring2.y:
                    self.running = False
                    break

            if self.bird.y + self.bird.dy > self.height:
                self.running = False
                break
            clock.tick(60)

class Bird:
    def __init__(self,x,y,dy,r = 15):
        self.x = x
        self.y = y
        self.dy = dy
        self.G = 0
        self.r = r


    def beveg(self):
        self.G = 0.35
        self.dy = 0
        self.dy -= 7 

    def gravitasjon(self):
        self.dy += self.G
        self.y += self.dy

    def render(self,vindu):
        self.fugl = pg.transform.scale(fugl,(6*self.r,6*self.r))
        self.vinkel = 0

        #bruker en vinkel som fuglen får basert på hvor stor hastighet den har i y-retning
        if self.dy < 0:
            self.vinkel = 20
        
        elif self.dy > 8:
            self.vinkel = -40
        
        elif self.dy > 0:
            self.vinkel = -20


        elif self.dy == 0:
            self.vinkel = 0

        print(self.dy)
        self.rotert = pg.transform.rotate(self.fugl,self.vinkel)
        self.ny_fugl = self.rotert.get_rect(center=(self.x, self.y))

        vindu.blit(self.rotert, self.ny_fugl.topleft) #.topleft fordi øverst til venstre er "sentrum" av fuglen. 

class Hindring:
    def __init__(self,x):
        self.x = x
        self.y = r.randint(HEIGHT // 3, HEIGHT-HEIGHT//3 )
        self.diff = HEIGHT // 4
        self.width = WIDTH // 8

    def nyRunde(self):
        """
        metode som resetter x-posisjon
        kalles når den aktuelle hindringen er på venstre side av skjermen
        """
        self.x = WIDTH
        self.y = r.randint(HEIGHT // 3, HEIGHT-HEIGHT//3)
  
    def beveg(self):
        if self.x + self.width < 0:
            self.nyRunde()
        else:
            self.x -= 2

    def render(self,vindu):
        pg.draw.rect(vindu,(0,255,0),pg.Rect(self.x,0,self.width,self.y)) #første halvdel av hindringen
        pg.draw.rect(vindu,(0,255,0),pg.Rect(self.x,self.y+self.diff,self.width,HEIGHT)) #andre halvdel

a = App()
a.run()





