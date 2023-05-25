# Autorrzy projektu
# Konrad Marciniak
# Martyna Toborek
# Maciej Standerski

import socket

# Ustawianie portu do nasłuchu
serverPort = 20001
clientPort = 20002
# Rozmiar bufora
bufferSize = 1024

# Tworzenie gniazda UDP
UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPServerSocket.bind(('',serverPort))

neighbours = [] # lista przechowujaca wezly "sasiadujace" z tym serwerem w danym polaczeniu, kod polaczenia i informacje, czy obecny serwer jest pierwszym wezlem w polaczeniu
# przechowuje ona tuple, ktorej postac wyglada nastepujaco:
# (ip poprzedniego wezla, ip kolejnego wezla, kod polaczenia, czy wezel poczatkowy [0=nie,1=tak])

#while block begin
while True:
    message, address = UDPServerSocket.recvfrom(bufferSize)
    message = message.decode('utf-8')
    print('Polaczenie z ', address)
    #print('Wiadomosc: ', message)
    #UDPServerSocket.sendto('Odebrano wiadomosc'.encode('utf-8'),address)

    nodesIPs = message.split(';')[1].split() # lista wezlow przeslana w pakiecie
    # pierwszy split oddziela adresy IP wezlow od wiadomosci
    # drugi split oddziela od siebie adresy IP i tworzy liste
    if len(nodesIPs) == 1:
        # jesli jest tylko jeden adres, znaczy to ze jest to adres serwera, czyli wiadomosc zostala dostarczona
        message = '0;;' + message.split(';',2)[2] # usuniecie adresu ip serwera z listy
        print('Otrzymano wiadomosc:\n ', message.split(';')[3])
        previousNodeIP = address[0]
        UDPServerSocket.sendto(message.encode('utf-8'),(previousNodeIP,serverPort))
    else:
        connection_code = int(message.split(';')[2]) # kod polaczenia
        print(nodesIPs)
        # sa dwie opcje, 1. pakiet wysylany jest do serwera, 2. -//- do klienta
        # Opcja 2 - wysylanie z serwera do klienta
        if (address[0],connection_code) in [(t[1],t[2]) for t in neighbours]:
            print('Wiadomosc zwrotna: ', message)
            for i in range(len(neighbours)):
                if address[0] == neighbours[i][1] and connection_code == neighbours[i][2]:
                    toRemove = i
                    previousNodeIP = neighbours[i][0]
                    break
            if neighbours[toRemove][3] == 1:
                # jesli wezel jest piwerwszym wezlem sieci, to wyslij do klienta przez clientPort
                neighbours.pop(toRemove) # usun sasiadow z pamieci
                UDPServerSocket.sendto(message.encode('utf-8'),(previousNodeIP,clientPort))
            else:
                # jeslie wezel nie jest pierwszy, przeslij pakiet do kolejnego wezla
                neighbours.pop(toRemove)
                UDPServerSocket.sendto(message.encode('utf-8'),(previousNodeIP,serverPort))
                print('Wiadomosc posrednia do serwera: ' + message)
        # Opcja 1 - wysylanie wiadomosci od klienta do serwera
        else:
            print('Wiadomosc do serwera: ', message)
            print(nodesIPs)
            nextNodeIP = nodesIPs[1] # nastepny wezel
            # jesli nie znaleziono takiego polaczenia, dodaj go do listy neighbours i przeslij wiadomosc do kolejnego wezla
            isFirst = int(message.split(';')[0])
            # usun pierwszy wskaznik okreslajacy, czy wezel jest pierwszy
            message = message.split(';',1)[1] # rozwiazanie z https://www.geeksforgeeks.org/python-removing-initial-word-from-string/
            # usun pierwszy adres ip wezla na liscie, jest to wezel obecnego serwera
            message = message.split(' ',1)[1]
            # dodaj informacje o polaczeniu do listy neighbours
            neighbours.append((address[0],nextNodeIP,connection_code,isFirst))
            # wyslij wiadomosc do nastepnego wezla
            message = '0;' + message
            UDPServerSocket.sendto(message.encode('utf-8'),(nextNodeIP,serverPort))
            print('Wiadomosc posrednia zwrotna: ' + message)
# koniec petli while