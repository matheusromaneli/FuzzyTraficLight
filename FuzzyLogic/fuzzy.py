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
# Variáveis ​​Linguisticas. Termos Linguisticos 
### Se Antecedente Então Consequente 
### Novos objetos Antecedent / Consequent possuem variáveis ​​de universo e número de associação
pessoa = ctrl.Antecedent(np.arange(0,1001,1), 'pessoas')
veiculo = ctrl.Antecedent(np.arange(0,1001,1), 'veiculos')

aberto = ctrl.Consequent(np.arange(0,100,1), 'tempo')
# Fuzzificação 
pessoa['r1'] = fuzz.trapmf(pessoa.universe, [0,  0,  5, 10])
pessoa['r2'] = fuzz.trapmf(pessoa.universe, [5, 10, 15, 20])
pessoa['r3'] = fuzz.trapmf(pessoa.universe, [15, 20, 25, 30])
pessoa['r4'] = fuzz.trapmf(pessoa.universe, [25, 30, 35, 40])
pessoa['r5'] = fuzz.trapmf(pessoa.universe, [35, 40, 1000, 1001])

veiculo['v1'] = fuzz.trapmf(veiculo.universe, [0,0, 5,10])
veiculo['v2'] = fuzz.trapmf(veiculo.universe, [5, 10, 15, 25])
veiculo['v3'] = fuzz.trapmf(veiculo.universe, [15,25, 30,40])
veiculo['v4'] = fuzz.trapmf(veiculo.universe, [30,40, 50,60])
veiculo['v5'] = fuzz.trapmf(veiculo.universe, [50,60,1000,1001])

### Uma função de pertinência personalizada pode ser construída de forma interativa com uma API Pythonic
aberto['Mais Fechado']= fuzz.trimf(aberto.universe, [0,15, 30])
aberto['Fechado']= fuzz.trimf(aberto.universe, [15,30,45])
aberto['Equilibrado']= fuzz.trimf(aberto.universe, [30,45,60])
aberto['Aberto']= fuzz.trimf(aberto.universe, [45,60,75])
aberto['Mais Aberto'] = fuzz.trimf(aberto.universe, [60,75,100])

# Maquina de Inferência 
ruleMA  = ctrl.Rule((pessoa['r1'] & (veiculo['v3'] | veiculo['v4'] | veiculo['v5']))| (pessoa['r2'] & (veiculo['v4'] | veiculo['v5'])) | (pessoa['r3'] & veiculo['v5']), aberto['Mais Aberto'])
ruleA = ctrl.Rule((pessoa['r1'] & veiculo['v2']) | (pessoa['r2'] & veiculo['v3']) | (pessoa['r3'] & veiculo['v4']) | (pessoa['r4'] & veiculo['v5']), aberto['Aberto'])
ruleE  = ctrl.Rule ((veiculo ['v1'] & pessoa ['r1']) | (veiculo ['v1'] & pessoa ['r2']) | (veiculo ['v2'] & pessoa ['r2']) | (veiculo ['v2'] & pessoa ['r3']) | (veiculo ['v3'] & pessoa ['r3']) | (veiculo ['v3'] & pessoa ['r4']) | (veiculo ['v4'] & pessoa ['r4']) | (veiculo ['v4'] & pessoa ['r5']) | (veiculo ['v5'] & pessoa ['r5']), aberto['Equilibrado'])
ruleF = ctrl.Rule((pessoa['r3'] & veiculo['v1'])|(pessoa['r4'] & veiculo['v2'])|(pessoa['r5'] & veiculo['v3']), aberto['Fechado'])
ruleMF  = ctrl.Rule(((pessoa['r4'] | pessoa['r5'])& veiculo['v1']) | (pessoa['r5'] & veiculo['v2']), aberto['Mais Fechado'])
aberto_ctrl = ctrl.ControlSystem([ruleMA, ruleA, ruleE, ruleF, ruleMF])
aberto_simulator = ctrl.ControlSystemSimulation(aberto_ctrl)

### Simulação
#### Passe entradas para o ControlSystem usando rótulos Antecedent com *** Pythonic API ***
#Nota: se você gosta de passar muitas entradas de uma só vez, use .inputs (dict_of_data) ``



# Deffuzificação 
aberto_simulator.input['pessoas'] = 0
aberto_simulator.input['veiculos'] = 0
aberto_simulator.compute()
result = 0


width, height = 800,600
screen = window.Window(width, height)
inputs = keyboard.Keyboard()
screen.set_title("FUZZY: Semáforo Inteligente")

sinal_aberto = sprite.Sprite('src/semaforo_aberto.png')
sinal_aberto.set_position(600, 200 - sinal_aberto.height)
sinal_fechado = sprite.Sprite('src/semaforo_fechado.png')
sinal_fechado.set_position(600, 200 - sinal_fechado.height)

new_value = 0
n_roads = 5
road = Road(n_roads, width)
signal = True
npeoples = 0
end = False
fechou = False
closed_time = 0
opened_time = 0
while(not(end)):
    screen.set_background_color([13,13,44])
    new_value += screen.delta_time()
    if fechou:
        aberto_simulator.input['pessoas'] = npeoples
        npeoples = random.randint(0,100)

        aberto_simulator.input['veiculos'] = road.car_frequency
        aberto_simulator.compute()
        road.car_frequency = 0
        closed_time = float(aberto_simulator.output['tempo'])
        opened_time = 100 - float(aberto_simulator.output['tempo'])
        new_value = 0
        fechou = False
    if signal and new_value > opened_time + closed_time:
        fechou = True
        signal = False
    elif not(signal) and new_value > closed_time:
        signal = True
        fechou = False

    for i in range(n_roads):
        road.add_car(i)

    screen.draw_text(f"Tempo atual: {new_value:.2f}s",10,10, 24, (158,183,252))
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

