import socket
import sys
import random

nodesIPs = [] # lista adresow posredniczacych
# przyjmowanie argumentow
if len(sys.argv) < 4:
    print("Za mala liczba argumentow. Potrzeba przynajmniej 3 argumentow.")
    print("python cake_router_client.py <ip serwera docelowego> <ip 1-go wezla> <ip 2-go wezla> ... <ip n-go wezla>")
    sys.exit(1)
else:
    serverIP = sys.argv[1] # adres serwera docelowego
    # wczytywanie adresow wezlow z listy
    for i in range(2,len(sys.argv)):
        nodesIPs.append(sys.argv[i])

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
random.shuffle(nodesIPs) # wybor drogi przesylu danych pomiedzy wezlami
nodesIPs.append(serverIP) # dopisanie serwera docelowego na koncu listy
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
print("Odebrano wiadomosc od ", address, ": ", message.decode('utf-8'))
