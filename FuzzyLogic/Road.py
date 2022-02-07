#Importando as bibliotecas necessárias para a criação das rodovia para o carro
from Car import Car
from PPlay import window 
import pygame
import random

#Criando a classe para a rodovia
class Road():
    #Criando o objeto rodovia
    def __init__(self, n, width):
        self.initial_y = 200 #Posição inicial
        self.dy = 45 #Tamanho do carro
        self.n_roads = n #Numero de estradas
        self.car_frequency = 0 #Numeros de carros que passaram pelo sinal enquanto o mesmo estava aberto
        self.n_cars = 0 #Numero de carros atuais na tela
        self.roads = {} #Lista que armazena o numero de rodovias 
        for i in range(n):
            self.roads[f'R{i}'] = []

        self.limit = width
    #Adicionando os carros nas rodovias
    def add_car(self, road):
        if(road >= self.n_roads or (len(self.roads[f'R{road}']) != 0 and self.roads[f'R{road}'][-1].get_pos() < 0)):
            return
        else:
            self.n_cars += 1 #Adicionando mais 1 no numero de carros
            self.roads[f'R{road}'].append(Car(random.randint(1,2)))
    #Atualizando as rodovias
    def update(self, delta_time, signal):
        for road in self.roads:
            distance_last_car = 999999 #Maior distancia possivel para fazer a logica da distancia para o outro carro
            for car in self.roads[road]:
                current_car_pos = car.move(distance_last_car - car.get_pos(), delta_time) + car.image.width #Calculando a distancia entre os carros
                if current_car_pos > self.limit:
                    self.roads[road].pop(0)
                    self.car_frequency += 1 #Soma um quando o carro sai da tela
                    self.n_cars -= 1 #Diminui um quando o carro sai da tela
                    distance_last_car = 99999
                else:
                    if current_car_pos < 550 and signal:
                        car.slow(delta_time)
                    elif current_car_pos < 600 and signal:
                        car.stop()
                    distance_last_car = car.get_pos()
    #Desenhando as rodovias
    def draw(self):
        i = 0
        for road in self.roads:
            window.Window.get_screen().fill((50,50,50), pygame.Rect(0, self.initial_y + self.dy * i, self.limit, self.dy-3))
            for car in self.roads[road]:
                car.draw(self.initial_y + self.dy * i)
            
            i+=1

    
    
