# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import csv
import math


# A função lê o numero do arquivo de tempo do experimento da rampa a ser lido e
# retorna uma matriz de tempos e uma matriz de espaços aos tempos
def MruvTimesSpaces(filenumber):
    times = []
    spaces = [10, 20, 30]
    first_line = True
    for i in range(1,5):
        for row in csv.reader(open("mruv/experimento" + str(filenumber) + '.csv', 'rt')):
            if first_line == False:
                t1 = float(row[0])
                t2 = float(row[1])
                t3 = float(row[2])
                times.append(t1)
                times.append(t2)
                times.append(t3)
            first_line = False
        return times, spaces

# A função lê o numero do arquivo de tempo do experimento do pendulo a ser lido e
# retorna uma matriz de tempos e uma matriz de espaços aos tempos
def pendulumTimesSpaces(filenumber):
    # Função que recebe um arquivo "filenametoolbox" contendo dados do acelerômetro
    # e retorna os tempos nos pontos altos e baixos da trajetória do pêndulo.
    times = []
    points = []
    first_line = True
    before10s = True
    timesnew = []
    pointsnew = []
    for row in csv.reader(open("pendulo/experimento" + str(filenumber) + ".csv", 'rt')):
        # Firulas/gambiarras iniciais
        if first_line == True:
            first_line = False
        elif before10s == True:
            if float(row[0]) >= 10.0:
                before10s = False
        elif float(row[0]) <= 130.0:
            times.append(float(row[0]))
            point = float(row[4])
            points.append(point)
        else:
            break
    aux = times[0]
    for i in range(len(times)):
        times[i] -= aux
    dt = 0.55
    diff = 0
    downFound = False
    upFound = True
    searches = 0
    i = 0
    j = 0
    while i < len(times) and j < len(times):

        j = i + 1
        while diff <= dt and j < len(times):
            if points[i] > points[j]:
                i = j
                diff = 0
            else:
                diff = times[j] - times[i]
                j += 1
        timesnew.append(times[i])
        pointsnew.append(points[i])
        diff = 0

        j = i + 1
        while diff <= dt and j < len(times):
            if points[i] < points[j]:
                i = j
                diff = 0
            else:
                diff = times[j] - times[i]
                j += 1

        timesnew.append(times[i])
        pointsnew.append(points[i])
        diff = 0

    angles = []
    times = []

    osc = 0

    for i in range(0,len(pointsnew),2):
        ang = (math.pi / 6) * (pointsnew[i+1]-pointsnew[i])/(pointsnew[1]-pointsnew[0])
        if (ang > degtorad(4.5)):
            angles.append(((-1)**(osc))*ang)
            times.append(timesnew[i])
            angles.append(0)
            times.append(timesnew[i+1])
            osc+=1

    # y,v,t = eulerCromer(math.pi/6, 0.05, "pendulo")
    # plt.plot(times, angles,"bo",t,y,"r")
    # plt.ylabel('angulo (°)')
    # plt.xlabel('tempo (s)')
    # plt.show()

    return times, angles

def g():
    return 9.8

# retorna a aceleração da bicicleta para algoritmos numéricos,
# com base na função horária do mruv, utilizando
# g = 9.8
# seno da inclinação = 0.0784591
# aceleração da resistencia ao giro = 0.0295/v0
def accMruv(v0):
    if v0 == 0:
        return  g() * 0.0784591
    else:
        return  g() * 0.0784591 - 0.0295/v0

#retorna aceleração do pendulo para algoritmos numéricos,
# com base na equação do pendulo, utilizando
# g = 9.8 m/s²
# massa do pendulo = 0.85kg
# coeficiente de resistencia do ar = 1.5
def accPendulum(y, v0):
    return (- 9.8 * y) / 0.85 + 1.5*v0**2

# recebe o espaço inicial y0, dt e o tipo de movimento movement ("pendulum" ou "mruv"),
# implementa o metodo de Euler-Cromer e retorna vetores de velocidades, acelerações,
# espaços e tempos
def eulerCromer (y0, dt, movement):
    t0 = 0
    i = 0
    v = []
    y = []
    a = []
    t = []
    y.append(y0)
    v.append(0)
    t.append(t0)

    if(movement == "mruv"):
        a.append(accMruv(v[i]))
        while(y[i] <= 30):
            t0 += dt
            a.append(accMruv(v[i]))
            v.append(v[i] + dt * a[i + 1])
            y.append(y[i] + v[i + 1] * dt)
            t.append(t0)
            i += 1
    else:
        a.append(accPendulum(y[i], v[i]))
        while(t[i] < 120):
            t0 += dt
            a.append(accPendulum(y[i], v[i]))
            v.append(v[i] + dt * a[i + 1])
            y.append(y[i] + v[i + 1] * dt)
            t.append(t0)
            i += 1

    return y, v, a, t

# recebe o espaço inicial y0, dt e o tipo de movimento movement ("pendulum" ou "mruv"),
# implementa o metodo de Euler-Richardson e retorna vetores de velocidades, acelerações,
# espaços e tempos
def eulerRichardson(y0, dt, movement):
    v = []
    y = []
    a = []
    t = []
    i = 0
    t0 = 0
    dtmid = dt / 2
    v.append(0)
    y.append(y0)
    t.append(t0)

    if movement == "mruv":
        a.append(accMruv(v[i]))
        while y[i] <= 30:
            t0 += dt
            vmid = v[i] + dtmid * accMruv(v[i])
            ymid = y[i] + dtmid * vmid

            a.append(accMruv(vmid))

            v.append(v[i] + dt * a[i + 1])
            y.append(y[i] + dt * vmid)
            t.append(t0)

            i += 1

    else:
        a.append(accPendulum(y[i], v[i]))
        while t[i] < 120:
            t0 += dt
            vmid = v[i] + dtmid * accPendulum(y[i], v[i])
            ymid = y[i] + dtmid * v[i]

            a.append(accPendulum(ymid, vmid))

            v.append(v[i] + dt * a[i + 1])
            y.append(y[i] + dt * vmid)
            t.append(t0)

            i += 1
    return y, v, a, t

# transforma graus em radianos
def degtorad(deg):
    return (2*math.pi*deg/360)


def main():
    dt = float(input("Informe dt:\n"))

    print("Analisando experimento da rampa...")
    corridas = []
    acelCorridas = []
    for i in range(1, 6):
        tempo, espaco = MruvTimesSpaces(i)
        richS, richV, richA, richT = euler(0, dt, "mruv")
        fig = plt.figure(1)

        plt.subplot(221)
        plt.title("x(t)")
        plt.plot(tempo, espaco, 'o', label='Oficial')
        plt.plot(richT, richS, label='Euler-Richardson')
        plt.ylabel('Espaço (m)')
        plt.xlabel('Tempo (s)')
        plt.legend()
        plt.subplot(222)
        plt.title("v(t)")
        plt.plot(richT, richV, label='Euler-Richardson')
        plt.ylabel('Velocidade (m/s)')
        plt.xlabel('Tempo(s)')
        plt.legend()

        plt.subplot(223)
        plt.title("a(t)")
        plt.plot(richT, richA, label='Euler-Richardson')
        plt.ylabel('Aceleração (m/s²)')
        plt.xlabel('Tempo (s)')
        plt.legend()

        plt.savefig('rampa' + str(i))
        plt.close(fig)

    print("Analisando o experimento do pêndulo...")

    for i in range(1, 6):
        tempo, angulos = pendulumTimesSpaces(i)
        cromerS, cromerV, cromerA, cromerT = eulerCromer(math.pi/6, dt, "pendulum")
        fig = plt.figure(1)

        plt.subplot(221)
        plt.title("angulo(t)")
        plt.plot(tempo, angulos, 'o', label='Oficial')
        plt.plot(cromerT, cromerS, label='Euler-Cromer')
        plt.ylabel('angulo (rad)')
        plt.xlabel('Tempo (s)')
        plt.legend()

        plt.subplot(222)
        plt.title("v(t)")
        plt.plot(cromerT, cromerV, label='Euler-Cromer')
        plt.ylabel('Velocidade (rad/s)')
        plt.xlabel('Tempo(s)')
        plt.legend()

        plt.subplot(223)
        plt.title("a(t)")
        plt.plot(cromerT, cromerA, label='EulerCromer')
        plt.ylabel('Aceleração (rad/s²)')
        plt.xlabel('Tempo (s)')
        plt.legend()

        plt.savefig('pendulo' + str(i))
        plt.close(fig)

    print("Finalizado.")

if __name__ == '__main__':
    main()
