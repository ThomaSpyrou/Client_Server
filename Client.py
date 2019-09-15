'''Client has the option of read, write and exit in a list with flights'''
import sys
import socket


class Client(object):
    def __init__(self):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = ''
        self.port = 7777

    def connect(self):
        # connect with the socket and send chosen option
        print('1 --> Read, 2 --> Write 3 --> Exit')
        conn = (self.addr, self.port)

        self.socket.connect(conn)

        while True:
            message = input('Enter your message: ')
            if message == 'Exit':
                print('EXIT')
                self.socket.close()
                sys.exit()

            self.socket.sendall(message.encode('UTF-8'))
            data = self.socket.recv(1024).decode('UTF-8')
            print(data)

        self.socket.close()


if __name__ == "__main__":
    client = Client()
    client.connect()
