from PPlay import window
from PPlay import keyboard
from PPlay import sprite
from Road import Road

width, height = 800,600
screen = window.Window(width, height)
inputs = keyboard.Keyboard()
screen.set_title("FUZZY: Semáforo Inteligente")

sinal_aberto = sprite.Sprite('src/semaforo_aberto.png')
sinal_aberto.set_position(600, 200 - sinal_aberto.height)
sinal_fechado = sprite.Sprite('src/semaforo_fechado.png')
sinal_fechado.set_position(600, 200 - sinal_fechado.height)

current_time = 0
n_roads = 5 #Numero de rodovias
road = Road(n_roads, width) #Chamada da classe rodovias
signal = True #Estado do sinal
npeoples = 0 #Numero de pessoas querendo atravessar
end = False #Controle do termino da simulação
fechou = False #Controle do sinal
closed_time = 50 #Tempo que deverá ficar fechado
opened_time = 50 #Tempo que deverá ficar aberto
while(not(end)):
    screen.set_background_color([13,13,44])
    current_time += screen.delta_time()
    if fechou:
        road.car_frequency = 0
        current_time = 0
        fechou = False

    if signal and current_time > opened_time:
        fechou = True
        signal = False
        current_time = 0
    elif not(signal) and current_time > closed_time:
        signal = True
        fechou = False
        current_time = 0

    for i in range(n_roads):
        road.add_car(i)

    screen.draw_text(f"Tempo atual: {current_time:.2f}s",10,10, 24, (158,183,252))
    screen.draw_text(f"Duração do sinal aberto: {opened_time:.2f} | Duração do sinal fechado: {closed_time:.2f} ",10,34, 24, (252,241,173))
    screen.draw_text(f"Veículos na tela: {road.n_cars} | Vazão de veículos: {road.car_frequency} | Pessoas: {npeoples} | Sinal: {signal}",10,58, 24, (252,173,173))
    if(inputs.key_pressed('esc')):
        signal = not(signal)
    road.update(screen.delta_time(), not(signal))
    road.draw()
    if(signal):
        sinal_aberto.draw()
    else:
        sinal_fechado.draw()
    screen.update()
