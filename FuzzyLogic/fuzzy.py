# Modelagem de semaforos inteligentes usando lógica fuzzy
#### Para o nosso exemplo o tempo de semaforo varia de 0-100, em que 0 indica estar fechado e 100 aberto. 
from skfuzzy import control as ctrl
import skfuzzy as fuzz
import numpy as np
from PPlay import window
from PPlay import keyboard
from PPlay import sprite
from Road import Road
import random
import matplotlib as plt

# Variáveis ​​Linguisticas. Termos Linguisticos 
### Se Antecedente Então Consequente 
### Novos objetos Antecedent / Consequent possuem variáveis ​​de universo e número de associação
pessoa = ctrl.Antecedent(np.arange(0,60,1), 'pessoas')
veiculo = ctrl.Antecedent(np.arange(0,100,1), 'veiculos')

aberto = ctrl.Consequent(np.arange(0,100,1), 'tempo')
# Fuzzificação 
pessoa['muito baixo'] = fuzz.trapmf(pessoa.universe, [0,  0,  5, 10])
pessoa['baixo'] = fuzz.trapmf(pessoa.universe, [5, 10, 15, 20])
pessoa['medio'] = fuzz.trapmf(pessoa.universe, [15, 20, 25, 30])
pessoa['alto'] = fuzz.trapmf(pessoa.universe, [25, 30, 35, 40])
pessoa['muito alto'] = fuzz.trapmf(pessoa.universe, [35, 40, 60, 60])

veiculo['muito baixo'] = fuzz.trapmf(veiculo.universe, [0,0, 5,10])
veiculo['baixo'] = fuzz.trapmf(veiculo.universe, [5, 10, 15, 25])
veiculo['medio'] = fuzz.trapmf(veiculo.universe, [15,25, 30,40])
veiculo['alto'] = fuzz.trapmf(veiculo.universe, [30,40, 50,60])
veiculo['muito alto'] = fuzz.trapmf(veiculo.universe, [50,60,100,100])

### Uma função de pertinência personalizada pode ser construída de forma interativa com uma API Pythonic
aberto['Mais Fechado']= fuzz.trapmf(aberto.universe, [0,0,15, 30])
aberto['Fechado']= fuzz.trimf(aberto.universe, [15,30,45])
aberto['Equilibrado']= fuzz.trimf(aberto.universe, [30,45,60])
aberto['Aberto']= fuzz.trimf(aberto.universe, [45,60,75])
aberto['Mais Aberto'] = fuzz.trapmf(aberto.universe, [60,75,100,100])

# Maquina de Inferência 
ruleMA  = ctrl.Rule((pessoa['muito baixo'] & (veiculo['medio'] | veiculo['alto'] | veiculo['muito alto']))| (pessoa['baixo'] & (veiculo['alto'] | veiculo['muito alto'])) | (pessoa['medio'] & veiculo['muito alto']), aberto['Mais Aberto'])
ruleA = ctrl.Rule((pessoa['muito baixo'] & veiculo['baixo']) | (pessoa['baixo'] & veiculo['medio']) | (pessoa['medio'] & veiculo['alto']) | (pessoa['alto'] & veiculo['muito alto']), aberto['Aberto'])
ruleE  = ctrl.Rule ((veiculo ['muito baixo'] & pessoa ['muito baixo']) | (veiculo ['muito baixo'] & pessoa ['baixo']) | (veiculo ['baixo'] & pessoa ['baixo']) | (veiculo ['baixo'] & pessoa ['medio']) | (veiculo ['medio'] & pessoa ['medio']) | (veiculo ['medio'] & pessoa ['alto']) | (veiculo ['alto'] & pessoa ['alto']) | (veiculo ['alto'] & pessoa ['muito alto']) | (veiculo ['muito alto'] & pessoa ['muito alto']), aberto['Equilibrado'])
ruleF = ctrl.Rule((pessoa['medio'] & veiculo['muito baixo'])|(pessoa['alto'] & veiculo['baixo'])|(pessoa['muito alto'] & veiculo['medio']), aberto['Fechado'])
ruleMF  = ctrl.Rule(((pessoa['alto'] | pessoa['muito alto'])& veiculo['muito baixo']) | (pessoa['muito alto'] & veiculo['baixo']), aberto['Mais Fechado'])
aberto_ctrl = ctrl.ControlSystem([ruleMA, ruleA, ruleE, ruleF, ruleMF])
aberto_simulator = ctrl.ControlSystemSimulation(aberto_ctrl)

### Simulação
#### Passe entradas para o ControlSystem usando rótulos Antecedent com *** Pythonic API ***
# Defuzzificação 
aberto_simulator.input['pessoas'] = 35
aberto_simulator.input['veiculos'] = 35
aberto_simulator.compute()


print(aberto_simulator.output['tempo'])

# pessoa.view(sim = aberto_simulator)
# veiculo.view(sim = aberto_simulator)
# aberto.view(sim = aberto_simulator)
# input()
width, height = 800,600
screen = window.Window(width, height)
inputs = keyboard.Keyboard()
screen.set_title("FUZZY: Semáforo Inteligente")

sinal_aberto = sprite.Sprite('src/semaforo_aberto.png')
sinal_aberto.set_position(600, 200 - sinal_aberto.height)
sinal_fechado = sprite.Sprite('src/semaforo_fechado.png')
sinal_fechado.set_position(600, 200 - sinal_fechado.height)

current_time = 0
n_roads = 3 #Numero de rodovias
road = Road(n_roads, width) #Chamada da classe rodovias
signal = True #Estado do sinal
npeoples = 0 #Numero de pessoas querendo atravessar
end = False #Controle do termino da simulação
fechou = False #Controle do sinal
closed_time = 0 #Tempo que deverá ficar fechado
opened_time = 0 #Tempo que deverá ficar aberto
while(not(end)):
    screen.set_background_color([13,13,44])
    current_time += screen.delta_time()
    if fechou: #Calculo Fuzzy para o tempo do sinal
        aberto_simulator.input['pessoas'] = npeoples  #Enviando o número de pessoas que desejam atravessar para realização do calculo
        npeoples = random.randint(0,50)

        aberto_simulator.input['veiculos'] = road.car_frequency #Enviando o fluxo de carros para realização do calculo
        aberto_simulator.compute() #Realizando a fuzzyficação
        road.car_frequency = 0
        closed_time = 100 - float(aberto_simulator.output['tempo'])
        opened_time = float(aberto_simulator.output['tempo'])
        current_time = 0
        fechou = False
    if signal and current_time > opened_time + closed_time:
        fechou = True
        signal = False
    elif not(signal) and current_time > closed_time:
        signal = True
        fechou = False

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

