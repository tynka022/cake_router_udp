import socket
import sys

# Przyjmowanie argumentów
if len(sys.argv) == 0:
    exit
else:
    serverIP = sys.argv[1]

# Ustawianie portu do nasłuchu
localPort = 20001
# Rozmiar bufora
bufferSize = 1024

UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPClientSocket.sendto(str.encode('Wiadomość dla servera'), (serverIP,localPort))

message = UDPClientSocket.recvfrom(bufferSize)
print(format(message))
