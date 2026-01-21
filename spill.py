import pygame as pg
import random as r

pg.init()

HEIGHT = 700
WIDTH = 600

bakgrunn = pg.image.load("bakgrunn.png")
bakgrunn = pg.transform.scale(bakgrunn, (WIDTH, HEIGHT))

fugl = pg.image.load("bird.png")

clock = pg.time.Clock()


class App:
    def __init__(self):
        self.height = HEIGHT
        self.width = WIDTH
        self._score = 0
        self._high_score = 0

    def setup(self):
        self.vindu = pg.display.set_mode((self.width, self.height))
        self.bird = Bird(self.width // 2, self.height // 2)

        self.hindring1 = Hindring(WIDTH)
        self.hindring2 = Hindring(WIDTH * 1.5)
        pg.display.set_caption("Flakse-Fugl")

    def render(self):
        self.vindu.fill((255, 255, 255))
        self.vindu.blit(bakgrunn, (0, 0))

        self.bird.render(self.vindu)

        self.hindring1.render(self.vindu)
        self.hindring2.render(self.vindu)

        if self.bird.G == 0:  # før spillet er i gang, fuglen har 0 i G
            font = pg.font.SysFont(None, 17)
            text = font.render("Trykk på mellomrom / SPACE", True, (0, 0, 0))
            self.vindu.blit(text, (self.width // 2 - 75, self.height // 2 + 50))

        font_score = pg.font.SysFont(None, 30)
        hs_text = font_score.render(f"Highscore: {self._high_score}", True, (0, 0, 0))
        score_text = font_score.render(
            f"Nåværende score: {self._score}", True, (0, 0, 0)
        )
        self.vindu.blit(hs_text, (self.width // 11, self.height // 10))
        self.vindu.blit(score_text, (self.width // 11, (self.height // 10) + 35))

        pg.display.flip()

    def run(self):
        self.setup()
        self.running = True

        while self.running:
            self.render()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.bird.beveg()

            # Score skal ikke påvirkes før spillet er i gang, og G ikke er lik 0
            if self.bird.G != 0:
                self.bird.gravitasjon()
                self.hindring1.beveg()
                self.hindring2.beveg()

                # beveger blokkene først, slik at logikken nedenfor skal fungere som ønsket selv for den første blokken, som jo begynner med x = bredde

                # poengsum oppdateres i det en av hindringene går utenfor skjermen på venstre side. Da er fuglen akkurat kommet gjennom den 'andre' hindringen, slik at poenglogikken fungerer som ønsket.
                if self.hindring2.x == WIDTH:
                    self._score += 1
                elif self.hindring1.x == WIDTH:
                    self._score += 1

                # kollisjonssjekk

                fugl_rect = self.bird.hent_rect()

                # hindring 1
                for rect_objekt in self.hindring1.hent_rect():
                    if fugl_rect.colliderect(rect_objekt):  # .colliderect() gir en boolsk verdi som gir true dersom fugl_rect og rect_objekt kolliderer
                        self.dod()

                # hindring2
                for rect_objekt in self.hindring2.hent_rect():
                    if fugl_rect.colliderect(rect_objekt):
                        self.dod()

                if (
                    self.bird.hent_y() + self.bird.hent_dy() > self.height
                ):  # dersom fuglen faller ned på bunnen av skjermen er spillet også over
                    self.dod()

                if (
                    self.bird.hent_y() + self.bird.hent_dy() < 0
                ):  # dersom fuglen flyr over
                    self.bird.sett_y(0)

            clock.tick(60)

    def dod(self):
        if self._score > self._high_score:
            self._high_score = self._score

        self._score = 0
        self.bird.reset()

        self.hindring1.nyRunde()
        self.hindring2.nyRunde()  # for å få nye høyder på hindringen til den nye runden. denne metoden flytter og x, men det tas hånd om i linjene under

        self.hindring1.sett_x(self.width)
        self.hindring2.sett_x(self.width * 1.5)  # resetter fugl og hindringer til slik de var etter setup() metoden


class Bird:
    def __init__(self, x, y):
        self.y = y
        self.dy = 0
        self.G = 0
        self.r = 15
        self._start_y = y
        self.x = x
        self.fugl = pg.transform.scale(fugl, (6 * self.r, 6 * self.r))
        self.rect = pg.Rect(0, 0, 2 * self.r, 2 * self.r)

    def beveg(self):
        self.G = 0.35  # oppdateres kun når spillet først startes, holdes ellers konstant
        self.dy = 0
        self.dy -= 7

    def gravitasjon(self):
        self.dy += self.G
        self.y += self.dy

    def render(self, vindu):
        self.vinkel = 0
        # bruker en vinkel som fuglen får basert på hvor stor hastighet den har i y-retning

        if self.dy < 0:
            self.vinkel = 20

        elif self.dy > 8:
            self.vinkel = -40

        elif self.dy > 0:
            self.vinkel = -20

        elif self.dy == 0:
            self.vinkel = 0

        self.rotert = pg.transform.rotate(self.fugl, self.vinkel)
        self.ny_fugl = self.rotert.get_rect(center=(self.x, self.y))

        vindu.blit(self.rotert, self.ny_fugl)
        # pg.draw.rect(vindu,(0,0,0),self.hent_rect(),1) #denne linjen kan kommenteres inn/ut for å vise fuglens 'hitbox'

    def hent_rect(self):
        rect = pg.Rect(self.x, self.y - self.r, 2 * self.r, 2 * self.r)  # dette rect-objektet fungerer som en slags hitbox for fuglen
        rect.centerx = WIDTH // 2
        return rect

    def reset(self):
        self.G = 0
        self.dy = 0
        self.y = self._start_y

    def hent_y(self):
        return self.y

    def hent_dy(self):
        return self.dy

    def sett_y(self, parameter):
        self.y = parameter


class Hindring:
    def __init__(self, x):
        self.x = x
        self.y = r.randint(HEIGHT // 3, HEIGHT - HEIGHT // 3)
        self.diff = HEIGHT // 4
        self.width = WIDTH // 8

    def nyRunde(self):
        # resetter x-posisjon til å være på høyre ende av skjermen. Kalles for aktuelt hindring-objekt når det er utenfor på venstre side
        # bruker randint for å ha ulik høyde der åpningen er for hver runde

        self.x = WIDTH
        self.y = r.randint(HEIGHT // 3, HEIGHT - HEIGHT // 3)

    def beveg(self):
        if self.x + self.width < 0:  # dersom hindringen er på venstre side av skjermen
            self.nyRunde()
        else:
            self.x -= 2

    def sett_x(self, parameter):
        self.x = parameter

    def hent_rect(self):
        return [
            pg.Rect(self.x, 0, self.width, self.y),
            pg.Rect(self.x - 5, self.y - (HEIGHT // 20), self.width + 10, HEIGHT // 20),
            pg.Rect(self.x, self.y + self.diff, self.width, HEIGHT - (self.y + self.diff)),
            pg.Rect(self.x - 5, self.y + self.diff, self.width + 10, HEIGHT // 20),
        ]
        # henter rect-objekter for hindringen
        # 0: topp, hoved
        # 1: topp, kant
        # 2: bunn, hoved
        # 3: bunn, kant

    def render(self, vindu):
        rects = self.hent_rect()  # henter oppdaterte rect-objekter

        for rect in rects:  # tegner basert på de oppdaterte rect-objektene
            pg.draw.rect(vindu, (0, 255, 0), rect)  # grønn del
            pg.draw.rect(vindu, (0, 0, 0), rect, 1)  # kantlinje


a = App()
a.run()
