import socket
import socketserver
import threading
import time

# Ustawianie portu do nasłuchu
serverPort = 20001
clientPort = 20002
# Rozmiar bufora
bufferSize = 1024

# Tworzenie gniazda UDP

class MyUDPHandler(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.neighbours = [] # lista przechowujaca wezly "sasiadujace" z tym serwerem w danym polaczeniu, kod polaczenia i informacje, czy obecny serwer jest pierwszym wezlem w polaczeniu
    
        message = self.request[0].strip()
        socket = self.request[1]
        current_thread = threading.current_thread()
        #print("{} wrote:".format(self.client_address[0]))
        #print(data)
        
        message = message.decode('utf-8')
        print('Polaczenie z ', self.client_address[0])
        #print('Wiadomosc: ', message)
        #socket.sendto('Odebrano wiadomosc'.encode('utf-8'),address)

        nodesIPs = message.split(';')[1].split() # lista wezlow przeslana w pakiecie
        # pierwszy split oddziela adresy IP wezlow od wiadomosci
        # drugi split oddziela od siebie adresy IP i tworzy liste
        if len(nodesIPs) == 1:
            # jesli jest tylko jeden adres, znaczy to ze jest to adres serwera, czyli wiadomosc zostala dostarczona
            message = '0;;' + message.split(';',2)[2] # usuniecie adresu ip serwera z listy
            print('Otrzymano wiadomosc:\n ', message.split(';')[3])
            previousNodeIP = self.client_address[0]
            socket.sendto(message.encode('utf-8'),(previousNodeIP,serverPort))
        else:
            connection_code = int(message.split(';')[2]) # kod polaczenia
            #print(nodesIPs)
            # sa dwie opcje, 1. pakiet wysylany jest do serwera, 2. -//- do klienta
            # Opcja 2 - wysylanie z serwera do klienta
            if (self.client_address[0],connection_code) in [(t[1],t[2]) for t in self.neighbours]:
                #print('Wiadomosc zwrotna: ', message)
                for i in range(len(self.neighbours)):
                    if self.client_address[0] == self.neighbours[i][1] and connection_code == self.neighbours[i][2]:
                        toRemove = i
                        previousNodeIP = self.neighbours[i][0]
                        break
                if self.neighbours[toRemove][3] == 1:
                    # jesli wezel jest piwerwszym wezlem sieci, to wyslij do klienta przez clientPort
                    self.neighbours.pop(toRemove) # usun sasiadow z pamieci
                    socket.sendto(message.encode('utf-8'),(previousNodeIP,clientPort))
                else:
                    # jeslie wezel nie jest pierwszy, przeslij pakiet do kolejnego wezla
                    self.neighbours.pop(toRemove)
                    socket.sendto(message.encode('utf-8'),(previousNodeIP,serverPort))
                    #print('Wiadomosc posrednia do serwera: ' + message)
            # Opcja 1 - wysylanie wiadomosci od klienta do serwera
            else:
                #print('Wiadomosc do serwera: ', message)
                #print(nodesIPs)
                nextNodeIP = nodesIPs[1] # nastepny wezel
                # jesli nie znaleziono takiego polaczenia, dodaj go do listy self.neighbours i przeslij wiadomosc do kolejnego wezla
                isFirst = int(message.split(';')[0])
                # usun pierwszy wskaznik okreslajacy, czy wezel jest pierwszy
                message = message.split(';',1)[1] # rozwiazanie z https://www.geeksforgeeks.org/python-removing-initial-word-from-string/
                # usun pierwszy adres ip wezla na liscie, jest to wezel obecnego serwera
                message = message.split(' ',1)[1]
                # dodaj informacje o polaczeniu do listy self.neighbours
                self.neighbours.append((self.client_address[0],nextNodeIP,connection_code,isFirst))
                # wyslij wiadomosc do nastepnego wezla
                message = '0;' + message
                socket.sendto(message.encode('utf-8'),(nextNodeIP,serverPort))
                #print('Wiadomosc posrednia zwrotna: ' + message)


# przechowuje ona tuple, ktorej postac wyglada nastepujaco:
# (ip poprzedniego wezla, ip kolejnego wezla, kod polaczenia, czy wezel poczatkowy [0=nie,1=tak])

#while block begin

# koniec petli while

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass

if __name__ == "__main__":
    #with socketserver.UDPServer(('', serverPort), MyUDPHandler) as server:
     #   server.serve_forever()A

    server = ThreadedUDPServer(('', serverPort), MyUDPHandler)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True

    try:
        server_thread.start()
        #print("Server started at {} port {}".format(HOST, PORT))
        #while True: time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()
        server.server_close()
        exit()
