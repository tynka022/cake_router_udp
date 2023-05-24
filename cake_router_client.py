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

# ustawianie portu do nasluchu
localPort = 20001
# rozmiar bufora
bufferSize = 1024

# tworzenie gniazda
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# wysylanie wiadomosci do serwera
random.shuffle(nodesIPs) # wybor drogi przesylu danych pomiedzy wezlami
nodesIPs.append(serverIP) # dopisanie serwera docelowego na koncu listy
firstNodeIP = nodesIPs[0] # adres pierwszego wezla sieci
message_to_server = ' '.join(nodesIPs) # zapisane ip wezlow w kolejnosci
connetcion_code = random.randint(0,255)
message_to_server = message_to_server + ';' + str(connetcion_code) + ';' + inp # dopisanie wiadomosci
UDPClientSocket.sendto(message_to_server.encode('utf-8'), (firstNodeIP,localPort)) # wyslanie pakietu danych do pierwszego wezla sieci
# nasluchiwanie i oczekiwanie na odpowiedz z serwera
print("Oczekiwanie na odpowiedz z serwera...")
message, address = UDPClientSocket.recvfrom(bufferSize)
print("Odebrano wiadomosc od ", address, ": ", message.decode('utf-8'))
