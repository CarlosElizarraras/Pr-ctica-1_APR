import socket
from random import randint
from time import time


def matrizP():
    filas = ["1", "2", "3"];
    columnas = ["A", "B", "C"];
    alto = len(filas) + 1
    largo = len(columnas) + 1;
    matriz = []
    for i in range(alto):
        matriz.append([])
        for j in range(largo):
            matriz[i].append(" ")
    return generarMatrizInicial(matriz, filas, columnas)


def matrizA():
    filas = ["1", "2", "3", "4", "5"];
    columnas = ["A", "B", "C", "D", "E"];
    alto = len(filas) + 1
    largo = len(columnas) + 1;
    matriz = []
    for i in range(alto):
        matriz.append([])
        for j in range(largo):
            matriz[i].append(" ")
    return generarMatrizInicial(matriz, filas, columnas)


def generarMatrizInicial(matriz, filas, columnas):


    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if i == 0:
                if j == 0:
                    matriz[i][j] = " "
                else:
                    matriz[i][j] = columnas[j - 1]
            else:
                if j == 0:
                    matriz[i][j] = filas[i - 1]
                else:
                    matriz[i][j] = "-"
    return matriz


def verMatriz(matriz):
    alto = len(matriz)
    largo = len(matriz[0])
    for i in range(alto):
        for j in range(largo):
            print(matriz[i][j], "\t", end=" ")
        print()


def menu(case):
    print("\tElige una dificultad\t")
    print("1. Principiante")
    print("2. Avanzado")
    if case == 1:
        matrizp = matrizP()
        verMatriz(matrizp)
        jugar(matrizp, Client_conn)
        exit(0)
    if case == 2:
        matriza = matrizA()
        verMatriz(matriza)
        jugar(matriza, Client_conn)
        exit(0)


def colocar(matriz, sim, Client_conn):
    pos = str(Client_conn.recv(buffer_size), "ascii")
    print(pos)
    fila = int(pos[0])
    col = ord(pos[1]) - 64
    matriz[int(fila)][int(col)] = sim


def juegoAuto(matriz, sim, Client_conn):
    cont = 0
    while cont == 0:
        fila = randint(1, len(matriz) - 1)
        col = randint(65, 65 + (len(matriz) - 2)) - 64

        for i in range(len(matriz)):
            if i == fila:
                for j in range(len(matriz[0])):
                    if j == col:
                        if matriz[i][j] == "-":
                            msg = "Casilla elegida: " + str(fila) + (chr(col + 64))
                            matriz[i][j] = sim
                            cont += 1
                            verMatriz(matriz)



                    elif col <= 0 or col >= len(matriz[0]):

                        break;
            elif fila <= 0 or fila >= len(matriz):

                break;
    pos = str(fila) + (chr(col + 64))
    Client_conn.sendall(pos.encode())
    Client_conn.sendall(msg.encode())


def ganarH(matriz, sim):
    cont = 0
    for i in range(1, len(matriz)):
        cont = 0
        for j in range(1, len(matriz[0])):
            if matriz[i][j] == sim:
                cont += 1
                if cont is (len(matriz) - 1):
                    return 1
                    break;


def ganarV(matriz, sim):
    cont = 0
    for j in range(1, len(matriz[0])):
        cont = 0
        for i in range(1, len(matriz)):
            if matriz[i][j] == sim:
                cont += 1
                if cont is (len(matriz) - 1):
                    return 1
                    break;


def jugar(matriz, Client_conn):
    simJ = "x"
    simS = "o"
    cont = 0
    print("El jugador tira con: ", simJ)
    print("La máquina tira con: ", simS)
    long = (len(matriz) - 1) * (len(matriz) - 1)
    inicio = time()
    while cont < long:
        print("Turno del jugador\n")
        colocar(matriz, simJ, Client_conn)
        verMatriz(matriz)
        if ganarH(matriz, simJ) == 1:
            print("Ganó el jugador")
            break;
        if ganarV(matriz, simJ) == 1:
            print("Ganó el jugador")
            break;
        cont += 1;
        if cont >= long:
            print("Juego terminado: Es un empate")
            break
        print("Turno de la máquina\n")
        juegoAuto(matriz, simS, Client_conn)
        if ganarH(matriz, simS) == 1:
            print("Ganó la máquina")
            break;
        if ganarV(matriz, simS) == 1:
            print("Ganó la máquina")
            break;
        cont += 1
        if cont >= long:
            print("Juego terminado: Es un empate")
            break
    final = time()
    print("Duración de la partida: %.2f segundos" % (final - inicio))


HOST = "192.168.0.111"
PORT = 6085
buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen()
    print("El servidor TCP está disponible y en espera de solicitudes")

    Client_conn, Client_addr = TCPServerSocket.accept()
    with Client_conn:
        print("Conectado a", Client_addr)
        while True:
            case = int.from_bytes(Client_conn.recv(buffer_size), 'little')
            menu(case)

            if False:
                Client_conn.sendall(b"Adios")
                break
