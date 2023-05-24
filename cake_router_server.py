import socket

# Ustawianie portu do nasłuchu
localPort = 20001
# Rozmiar bufora
bufferSize = 1024

# Tworzenie gniazda UDP
UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPServerSocket.bind(('',localPort))

neighbours = [] # lista przechowujaca wezly "sasiadujace" z tym serwerem w danym polaczeniu

#while block begin
#while True:
message, address = UDPServerSocket.recvfrom(bufferSize)
message = message.decode('utf-8')
print('Polaczenie z ', address)
print('Wiadomosc: ', message)
#UDPServerSocket.sendto('Odebrano wiadomosc'.encode('utf-8'),address)

# przechowuje ona tuple, ktorej postac wyglada nastepujaco:
# (ip poprzedniego wezla, ip kolejnego wezla, kod polaczenia)
nodesIPs = message.split(';')[0].split() # lista wezlow przeslana w pakiecie
# pierwszy split oddziela adresy IP wezlow od wiadomosci
# drugi split oddziela od siebie adresy IP i tworzy liste
if len(nodesIPs) == 1:
    # jesli jest tylko jeden adres, znaczy to ze jest to adres serwera, czyli wiadomosc zostala dostarczona
    message = message.split(';',1)[1] # usuniecie adresu ip serwera z listy
    print('Otrzymano wiadomosc: ', message.split(';')[2])
    previousNodeIP = address[0]
    UDPServerSocket.sendto(message.encode('utf-8'),(previousNodeIP,localPort))
    pass
else:
    connection_code = int(message.split(';')[1]) # kod polaczenia
    nextNodeIP = nodesIPs[1] # nastepny wezel
    print(nodesIPs)
    # sa dwie opcje, 1. pakiet wysylany jest do serwera,2. -//- do klienta
    # Opcja 2 - wysylanie z serwera do klienta
    if (address[0],connection_code) in [(t[1],t[2]) for t in neighbours]:
        for i in neighbours:
            if address[0] == neighbours[i][1] and connection_code == neighbours[i][2]:
                toRemove = i
                previousNodeIP = neighbours[i][0]
                break
        neighbours.pop(toRemove)
        UDPServerSocket.sendto(message.encode('utf-8'),(previousNodeIP,localPort))
    # Opcja 1 - wysylanie wiadomosci od klienta do serwera
    else:
        # jesli jest wiecej adresow, usuwamy pierwszy adres z listy w wiadomosci i przesylamy pakiet dalej
        neighbours.append((address[0],nextNodeIP,connection_code))
        message = message.split(' ',1)[1] # rozwiazanie z https://www.geeksforgeeks.org/python-removing-initial-word-from-string/
        UDPServerSocket.sendto(message.encode('utf-8'),(nextNodeIP,localPort))
    print('Wiadomosc posrednia: ' + message)
    UDPServerSocket.sendto(message.encode('utf-8'),(nextNodeIP,localPort))
# while block end