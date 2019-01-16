from socket import socket, AF_INET, SOCK_STREAM
import pickle
import threading

def send_to_the_other(point,nowplayer):
        
        for csocket in players:
             if csocket!=nowplayer:
                csocket.send(point)

def receive_job(client_socket):
    while 1:
        point = pickle.loads(client_socket.recv(1024))
        point = pickle.dumps(point)
        threading.Thread(target=send_to_the_other,args=(point,client_socket,)).start()

players=[]

listener = socket(AF_INET, SOCK_STREAM)
listener.bind(('192.168.43.35', 12345))
listener.listen(5)

while 1:
    connection, addr = listener.accept()
    link=connection.recv(1024)
    players.append(connection)
    if len(players)==1:
	connection.send('black')
    else:
        connection.send('white')
    threading.Thread(target=receive_job,args=(connection,)).start()
connection.close()
print "Connection closed"

