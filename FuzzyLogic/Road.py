from Car import Car
from PPlay import window 
import pygame
import random
class Road():

    def __init__(self, n, width):
        self.initial_y = 200
        self.dy = 45 #size sprite of carro
        self.n_roads = n
        self.n_cars = 0
        self.roads = {}
        for i in range(n):
            self.roads[f'R{i}'] = []

        self.limit = width

    def add_car(self, road):
        if(road >= self.n_roads or (len(self.roads[f'R{road}']) != 0 and self.roads[f'R{road}'][-1].get_pos() < 0)):
            return
        else:
            self.n_cars += 1
            self.roads[f'R{road}'].append(Car(random.randint(1,2)))

    def update(self, delta_time, signal):
        for road in self.roads:
            distance_last_car = 999999
            for car in self.roads[road]:
                current_car_pos = car.move(distance_last_car - car.get_pos(), delta_time) + car.image.width
                if current_car_pos > self.limit:
                    self.roads[road].pop(0)
                    self.n_cars -= 1
                    distance_last_car = 99999
                else:
                    if current_car_pos < 550 and signal:
                        car.slow(delta_time)
                    elif current_car_pos < 600 and signal:
                        car.stop()
                    distance_last_car = car.get_pos()

    def draw(self):
        i = 0
        for road in self.roads:
            window.Window.get_screen().fill((100,100,100), pygame.Rect(0, self.initial_y + self.dy * i, self.limit, self.dy-3))
            for car in self.roads[road]:
                car.draw(self.initial_y + self.dy * i)
            
            i+=1

    
    