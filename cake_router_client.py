# Autorrzy projektu
# Konrad Marciniak
# Martyna Toborek
# Maciej Standerski

import socket
import random
import sys

nodesIPs = [] # lista adresow posredniczacych
# Wczytywanie adresow IP serwerow z pliku konfiguracyjnego
file_name = "cake_router.conf" # nazwa pliku konfiguracyjnego
f = open(file_name,"r") # obiekt przchowujacy plik konfiguracyjny do odczytu
for line in f:
    if line.find('#') == -1: # jesli linijka nie jest komentarzem, to...
        line = line.split('\n')[0] # usun z linijki znak przejscia do nastepnej linijki '\n'
        if len(line.split()) > 1: # jesli w linijce jest wiecej niz jeden wyraz, przerwij program
            print("Błąd! W pliku " + file_name + " w jednej linijce musi się znajdować dokladnie jeden adres.")
            sys.exit(1)
        if len(line.split()) == 0: # jesli linijka jest pusta, przejdz do nastepnej linii
            continue
        # jesli w linii nie ma wyrazu w postaci IP xxx.xxx.xxx.xxx, gdzie xxx to liczba calkowita z przedzialu [0,255], to przerwij program
        if any(c.isalpha() for c in line) or line.count('.') != 3:
            print("Błąd! W pliku " + file_name + " znajduje się linijka, w ktorej adres IP zostal podany w zlej postaci.")
            sys.exit(1)
        for nr in line.split('.'):
            if int(nr) > 255: # sprawdzanie, czy liczby w adresie IP sa z zakresu [0,255]
                print("Błąd! W pliku " + file_name + " znajduje sie adres ze zla wartoscia.")
                sys.exit(1)
        nodesIPs.append(line)
# sprawdzenie, czy zostaly wczytane przynajmniej 3 adresy IP
if len(nodesIPs) < 3:
    print("W pliku " + file_name + " jest za malo adresow IP. Wymagane przynajmniej 3 adresy.")
    exit()

serverIP = nodesIPs[-1]

inp = input("Wpisz wiadomosc do przeslania:\n")

# port do wysylania
sendingPort = 20001
# port do nasluchu
recvingPort = 20002
# rozmiar bufora
bufferSize = 1024

# tworzenie gniazda do wysylania
UDPClientSocketSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# tworzenie gniazda do nasluchu
UDPClientSocketRecv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPClientSocketRecv.bind(('',recvingPort))
# wysylanie wiadomosci do serwera
firstNodeIP = nodesIPs[0] # adres pierwszego wezla sieci
nodes = ' '.join(nodesIPs) # zapisane ip wezlow w kolejnosci
connetcion_code = random.randint(0,255)
# pakiet danych przesylany jest w postaci: <czy wezel jest pierwszym wezlem posredniczacym>;[lista adresow ip wezlow];<kod polaczenia>;wiadomosc
message_to_server = '1;' + nodes + ';' + str(connetcion_code) + ';' + inp # dopisanie wiadomosci
UDPClientSocketSend.sendto(message_to_server.encode('utf-8'), (firstNodeIP,sendingPort)) # wyslanie pakietu danych do pierwszego wezla sieci
UDPClientSocketSend.close()
# nasluchiwanie i oczekiwanie na odpowiedz z serwera, nasluchiwanie nastepuje na innym porcie
print("Oczekiwanie na odpowiedz z serwera...")
message, address = UDPClientSocketRecv.recvfrom(bufferSize)
print("Odebrano wiadomosc od ", address, ": ", message.decode('utf-8').split(';')[3])
