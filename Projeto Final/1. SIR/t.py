
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from math import *

figure = plt.figure()
graph = figure.gca(projection='3d')
graph.set_zlabel('z')
graph.set_xlabel('x')
graph.set_ylabel('y')



# assumindo:
# eixo x = comprimento
# eixo y = largura
# eixo z = altura
width , length = 70.0, 144.0        # dimensões do campo
width_H , height_H = 5.6, 5.0       # dimensões do H

coord_x_H = length
coord_y_H = width/2
coord_z_H = 3.0

left_H_x = [width, width]
left_H_y = [(coord_y_H - (width_H/2)),(coord_y_H - (width_H/2))]
left_H_z = [0, height_H]

right_H_x = [width, width]
right_H_y = [(coord_y_H + (width_H/2)),(coord_y_H + (width_H/2))]
right_H_z = [0, height_H]


horizontal_H_x = [width,width]
horizontal_H_y = [(coord_y_H - (width_H/2)),(coord_y_H + (width_H/2))]
horizontal_H_z = [coord_z_H,coord_z_H]

graph.plot(left_H_x, left_H_y, left_H_z, color='b')
graph.plot(right_H_x, right_H_y, right_H_z, color='b')
graph.plot(horizontal_H_x, horizontal_H_y, horizontal_H_z, color='b')


# Calculo da trajetória a partir da posição escolhida pelo jogador
def throw(coord_x, coord_y, init_ball_speed, init_theta, init_phi):
    init_ball_speed = float(init_ball_speed)     # velocidade inicial da bola
    g = 9.81                                     # gravidade
    m = float(0.4)                               # massa da bola de rugby
    
    h = 0.01                                     # passo

    # considerando a resistencia do ar
    c = 0.14                          # constante de arrasto 
    d = 0.0172                        # diametro em metro
    area = (pi*d**2)/4.0         # area da bola em metro^2
    ro = 1.2                          # densidade em kg/m^3
    k = (c*ro*area)/2.0               # constante 
    
    # velocidade inicial em cada eixo
    init_speed_x = init_ball_speed * sin(init_theta) * sin(init_phi)
    init_speed_y = init_ball_speed * cos(init_theta) * sin(init_phi)
    init_speed_z = init_ball_speed * cos(init_phi)

    init_coord_x = float(coord_x)  # posição inicial da bola no eixo x 
    init_coord_y = float(coord_y)  # posição inicial da bola no eixo y 
    init_coord_z = 0.0             # posição inicial da bola no eixo z 

    # em x ----> vx' = -kvx/m e x' = vx
    # em y ----> vy' = -kvy/m e y' = vy
    # em z ----> vz' = -kvz/m - g e z' = vz

    vet_x=[]
    vet_y=[]
    vet_z=[]
    speed_x = init_speed_x
    speed_y = init_speed_y
    speed_z = init_speed_z

    vet_x.append(init_coord_x)
    vet_y.append(init_coord_y)
    vet_z.append(init_coord_z)

    while vet_x[-1] < 70 and vet_z[-1]>=0:
        x = vet_x[-1] + h * speed_x
        y = vet_y[-1] + h * speed_y
        z = vet_z[-1] + h * speed_z

        speed_x -= h*(k/m)*speed_x
        speed_y -= h*(k/m)*speed_y
        speed_z -= h*(((k/m)*speed_z) + g)

        vet_x.append(x)
        vet_y.append(y)
        vet_z.append(z)

        dist = sqrt((vet_x[-1]*2) + (vet_y[-1]*2))

    graph.plot(vet_x,vet_y,vet_z, color='red')
    check(vet_z[-1], vet_y[-1])
    plt.show()


def check(coord_z, coord_y):
    if (coord_z>coord_z_H) and coord_y < (coord_y_H + (width_H/2)) and coord_y > (coord_y_H - (width_H/2)):
        print("converteu")
    else:
        print("errou")


#Calculo da trajetória a partir da posição que gera o melhor angulo de visão
def best_angle(coord_try):
    pass

  

throw(50.0,20.0,17.0,pi/4.0,pi/4.0)