from random import randrange

width, height = 600, 150
gravity = 0.6

class rect_sub():
    def __init__(self, x, y, x2, y2):
        self.width = x2
        self.height = y2

        self.top = y
        self.bottom = y + y2
        self.right = x + x2
        self.left = x

    def __str__(self):
        return '<rect_sub{}>'.format((self.left, self.top, self.width, self.height))

    def move(self, movement):
        return rect_sub(self.left + movement[0],
                        self.top + movement[1],
                        self.width, self.height)

def collision(left, right):
    lrect = left.rect
    rrect = right.rect
    
    if isinstance(left, Dino):
        if left.isDucking:
            lrect = left.rect1

    offset = 5

    if lrect.right-offset > rrect.left+offset and lrect.left+offset < rrect.right-offset:
        
        if lrect.bottom <= rrect.top or lrect.top >= rrect.bottom:
            return False
        else:
            return True
    else: 
        return False

sprites_dict = {'dino': [147, 440], 'dino_ducking': [79, 236],
                'cacti-small': [68, 204], 'cacti-big': [101, 303], 
                'ptera': [61, 184]}

def load_sprite_sheet(sheetname):
    sprite = sprites_dict[sheetname]
    rect = rect_sub(0, 0, sprite[0], sprite[1])

    return rect


class Dino():
    def __init__(self):
        self.rect = load_sprite_sheet('dino')
        self.rect1 = load_sprite_sheet('dino_ducking')
        self.rect.bottom = int(0.98*height)
        self.rect.left = width/15
        self.index = 0
        self.counter = 0
        self.score = 0
        self.isJumping = False
        self.isDead = False
        self.isDucking = False
        self.isBlinking = False
        self.movement = [0, 0]
        self.jumpSpeed = 11.5

        self.stand_pos_width = self.rect.width
        self.duck_pos_width = self.rect1.width

    def checkbounds(self):
        if self.rect.bottom > int(0.98*height):
            self.rect.bottom = int(0.98*height)
            self.isJumping = False

    def update(self):
        if self.isJumping:
            self.movement[1] = self.movement[1] + gravity

        if not self.isDucking:
            self.rect.width = self.stand_pos_width
        else:
            self.rect.width = self.duck_pos_width

        self.rect = self.rect.move(self.movement)
        self.checkbounds()


class Cactus():
    def __init__(self, speed=5, size=randrange(0, 1)):
        if size == 1: self.rect = load_sprite_sheet('cacti-big')
        else: self.rect = load_sprite_sheet('cacti-small')
        self.rect.bottom = int(0.98 * height)
        self.rect.left = width + self.rect.width
        self.movement = [-1*speed, 0]

    def update(self):
        self.rect = self.rect.move(self.movement)


class Ptera():
    def __init__(self, speed=5):
        self.rect = load_sprite_sheet('ptera')
        self.ptera_height = [height*0.82, height*0.75, height*0.60]
        self.rect.centery = self.ptera_height[randrange(0, 3)]
        self.rect.left = width + self.rect.width
        self.movement = [-1 * speed, 0]

    def update(self):
        self.rect = self.rect.move(self.movement)


class game():

    def __init__(self):
        self.gamespeed = 4
        self.playerDino = Dino()
        self.counter = 0

        self.num_cacti = 0
        self.num_pteras = 0
        self.obstacles = []

    def reset(self):
        self.__init__()

    def step(self, action):
        gameOver = False
        reward = 0
        
        #Action == 0 is idle
        if action == 1: #Jumping
            if self.playerDino.rect.bottom == int(0.98*height):
                self.playerDino.isDucking = False
                self.playerDino.isJumping = True
                self.playerDino.movement[1] = -1*self.playerDino.jumpSpeed

        elif action == 2: #Ducking 
            if not (self.playerDino.isJumping and self.playerDino.isDead):
                self.playerDino.isDucking = True
        
        else:
            self.playerDino.isDucking = False
        
        for l in self.obstacles:
            l.movement[0] = -1*self.gamespeed
            if collision(self.playerDino, l):
                self.playerDino.isDead = True

        if self.num_cacti < 2:
            if self.num_cacti == 0:
                c = Cactus(self.gamespeed)
                self.num_cacti += 1
                self.obstacles.append(c)

            else:
                for l in self.obstacles:
                    if l.rect.right < width*0.7 and randrange(0, 50) == 10:
                        c = Cactus(self.gamespeed)
                        self.num_cacti += 1
                        self.obstacles.append(c)

        # if self.num_pteras == 0 and randrange(0, 200) == 10 and self.counter > 500:
        #     for l in self.obstacles:
        #         if l.rect.right < width*0.8:
        #             p = Ptera(self.gamespeed)
        #             self.num_pteras += 1
        #             self.obstacles.append(p)


        self.playerDino.update()

        [l.update() for l in self.obstacles]

        for l in self.obstacles:
            if l.rect.right < 40:
                self.obstacles.remove(l)

                reward += 10

                if isinstance(l, Cactus):
                    self.num_cacti -= 1
                elif isinstance(l, Ptera):
                    self.num_pteras -= 1


        if self.playerDino.isDead:
            gameOver = True

        if self.counter%700 == 699:
            self.gamespeed += 1

        self.counter += 1

        if len(self.obstacles) == 0:
            state = [701, 147] #default state
        else:
            last = self.obstacles[0].rect
            state = [last.bottom, last.left]

        return state, reward, gameOver
