import socket
import threading
import queue
import json
import time

# local_clock:
#       INCREMENT WHEN SENDING MESSAGE OR ACK
#       INCREMENT ON THE OCCURRENCE OF EVENTS


#########################################################################################################

lock = threading.Lock()

local_clock = 0
process_id = 0

general_address = "127.0.0.1"
processes_ports = [5051, 5052]

ip_server = "127.0.0.1"
port_server = 5050+process_id

# queue for communication between threads:
interest_queue = []

#########################################################################################################

def send_request(request):
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.connect((ip_geral, processes_ports[0]))
    s2.connect((ip_geral, processes_ports[1]))
    s1.sendall(request)
    s2.sendall(request)

def handle_client(conn, addr):
    print("oi")

def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip_server, port_server))
    server.listen()
    while True:
        conn, addr = server.accept()
        # thread to handle the client:
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()

def client():
    while True:
        interest = input("type 'yes' if this process will use the RESOURCE\nElse, type 'no'\n")
        global clock_local
        with lock:
            clock_local += 1
        if interest == "yes":
            interest_queue.append(True)
            
    
#################################################### MAIN ##################################################

if __name__ == "__main__":
    thread1 = threading.Thread(target=client)
    thread2 = threading.Thread(target=server)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
