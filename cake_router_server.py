import socket
import sys

# Przyjmowanie argumentów
#if len(sys.argv) == 0:
#    exit
#else:
#    localIP = sys.argv[1]

# Ustawianie portu do nasłuchu
localPort = 20001
# Rozmiar bufora
bufferSize = 1024

# Tworzenie gniazda UDP
UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

UDPServerSocket.bind(('localhost',localPort))
#UDPServerSocket.listen()

while True:
    bytes = UDPServerSocket.recvfrom(bufferSize)
    message = bytes[0]
    address = bytes[1]
    print('Połączenie z ', address)
    UDPServerSocket.sendto(str.encode('Odebrano wiadomość'),address)
