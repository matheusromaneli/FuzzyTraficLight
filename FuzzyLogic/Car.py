from PPlay import sprite
from PPlay import window

class Car():

    def __init__(self, acc):
        self.acc = acc
        self.acceleration = 10
        self.image = sprite.Sprite('src/carro_40.png')
        self.speed = self.image.width/3
        self.image.x = - self.image.width

    def move(self, distance, delta_time):
        if distance - abs(self.image.width) > 10:
            self.image.x += self.speed * delta_time
            if self.speed == 0:
                self.acceleration += 3
            else:
                self.acceleration += self.acc *delta_time
            self.speed += self.acceleration * delta_time
        else:
            self.speed = 0
            if self.acceleration - self.acc *delta_time > 0:
                self.acceleration -= self.acc *delta_time

        return self.image.x


    def slow(self, delta_time):
        if self.acceleration - self.acc *delta_time > 0:
                self.acceleration -= self.acc *delta_time
        
        if self.speed - self.acc * delta_time > 0:
            self.speed -= self.acc * delta_time

    def stop(self):
        self.speed = 0
        self.acceleration = 0

    def draw(self, y_off_set):
        self.image.y = y_off_set
        self.image.draw()

    def get_pos(self):
        return self.image.x