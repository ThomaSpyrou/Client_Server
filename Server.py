import socket
import threading
import json
import time
import random


class Server(object):
    def __init__(self):
        # shared list of flights for clients
        self.lock = threading.Lock()
        self.address = ''
        self.port = 7777
        self.flights = [
            {'code': 1, 'status': 'Arrival', 'time': '11:00'},
            {'code': 2, 'status': 'Departure', 'time': '10:00'},
            {'code': 3, 'status': 'Arrival', 'time': '12:00'},
            {'code': 4, 'status': 'Arrival', 'time': '13:00'},
            {'code': 5, 'status': 'Delay', 'time': '15:00'},
        ]

    def client_request(self, connection):
        # in this function depend on client's option they can read or write for both options there are
        # locks, so as to protect the shared list. data are sent back as a json

        while True:
            request = connection.recv(1024).decode('UTF-8')

            if request == 'Exit':
                connection.close()
            elif 'Read' in request:
                _, flight_code = request.split()

                with self.lock:
                    found_flight = None
                    time.sleep(random.randrange(0, 5))

                    for flight in self.flights:
                        if int(flight_code) == flight['code']:
                            found_flight = flight
                            break
                print(found_flight)
                if found_flight is not None:
                    connection.sendall(json.dumps(found_flight).encode('UTF-8'))
                else:
                    connection.sendall('Flight not found'.encode('UTF-8'))

            elif 'Write' in request:
                _, code, status, flight_time = request.split()

                self.lock.acquire()
                time.sleep(random.randrange(0, 5))
                new_flight = {
                    'code': int(code),
                    'status': status,
                    'time': flight_time
                }
                self.flights.append(new_flight)
                self.lock.release()

                connection.sendall('Flight added'.encode('UTF-8'))
            else:
                connection.sendall('Wrong choice'.encode('UTF-8'))
        connection.close()

    def start_listening(self):
        # in this function socket connection and create a thread for each client
        con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        con.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        con.bind((self.address, self.port))
        con.listen(1)

        while True:
            connection, address = con.accept()
            print(f'Connected by {address}')
            threading.Thread(target=self.client_request, args=(connection,)).start()
        con.close()


if __name__ == "__main__":
    server = Server()
    server.start_listening()


