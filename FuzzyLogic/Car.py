#Importando as bibliotecas necessárias para a criação do carro
from PPlay import sprite
from PPlay import window
from random import randint


# Classe Responsável pela criação, movimentação e ilustração dos carros usados para simular o sistema fuzzy.
class Car():
    #Criando o objeto do carro
    def __init__(self, acc):
        self.acc = acc
        self.acceleration = 10
        self.image = sprite.Sprite(f'src/carros/{randint(1,6)}.png')
        self.speed = self.image.width/3
        self.image.x = - self.image.width

    #Criando a função responsável pela movimentação do carro
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

    #Criando o sistema de freio do carro
    def slow(self, delta_time):
        if self.acceleration - self.acc *delta_time > 0:
                self.acceleration -= self.acc *delta_time
        
        if self.speed - self.acc * delta_time > 0:
            self.speed -= self.acc * delta_time
    #Criando a função de parada do carro
    def stop(self):
        self.speed = 0
        self.acceleration = 0
    #Criando a função de desenho do carro
    def draw(self, y_off_set):
        self.image.y = y_off_set
        self.image.draw()
    #Retornando a imagem do carro em sua respectiva posição atual
    def get_pos(self):
        return self.image.x
