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

server_ip = "127.0.0.1"
server_port = 5050+process_id

# global variable to keep track of the process interest on the resource ("yes", "no" or "using")
interest = "no"

#########################################################################################################

def send_requests(request):
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.connect((general_address, processes_ports[0]))
    s2.connect((general_address, processes_ports[1]))
    s1.sendall(request)
    s2.sendall(request)

def handle_client(conn, addr):
    print("oi")

def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen()
    while True:
        conn, addr = server.accept()
        # thread to handle the client:
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()

def client(): #sends the positive interest on the resource
    while True:
        resource = input("Type 'yes' if this process will use the RESOURCE\nElse, type 'no'\n\n")
        global interest
        with lock:
            interest = resource 
        global local_clock
        with lock:
            local_clock += 1
        if interest == "yes":
            request = {
                'clock': local_clock,
                'process_id': process_id
            }
            send_requests(request)
        time.sleep(2)
    
#################################################### MAIN ##################################################

if __name__ == "__main__":
    thread1 = threading.Thread(target=client)
    thread2 = threading.Thread(target=server)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
