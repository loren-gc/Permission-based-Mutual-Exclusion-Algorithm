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

processes_amount = 3
local_clock = 0
process_id = 0

general_address = "127.0.0.1"
processes_ports = [5051, 5052]

server_ip = "127.0.0.1"
server_port = 5050+process_id

# global variable to keep track of the process interest on the resource ("yes", "no" or "using")
interest = "no"
interest_queue = queue.PriorityQueue()
message_counter = 0

#########################################################################################################

def add_to_queue(item):
    global interest_queue
    with lock:
        interest_queue.put(item)

def use_resource():
    print("hey")

def send_nack(destiny_address, destiny_port):
    nack = {
        "type": "nack",
        "process_id": process_id
    }
    payload = json.dumps(nack).encode("utf-8") 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((destiny_address, destiny_port))
    s.sendall(payload)

def handle_request(message):
    item = [message["clock"], message["process_id"], message]
    add_to_queue(item)
    if message_counter == porcesses_amount:
        use_resource()

def handle_message(message): #it can be either a request or a nack
    global message_counter
    with lock:
        message_counter += 1
    if interest == "yes" && message["type"] == "request":
        handle_request(message)
    elif interest == "no" && message["type"] == "request":
        send_nack(general_ip, message["process_id"])

def clock_maintenance(foreign_clock):
    global clock_local
    with lock:
        if foreign_clock > local_clock:
            local_clock = foreign_clock + 1

def handle_client(conn, addr):
    try:
        data = conn.recv(1024)
        message = json.loads(data.decode("utf-8"))
        clock_maintenance(message["clock"])
        handle_message(message)
    except json.JSONDecodeError:
        print(f"[{addr}] Error: Invalid JSON!")

def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen()
    while True:
        conn, addr = server.accept()
        # thread to handle the client:
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()

def send_requests(request):
    global local_clock
    with lock:
        local_clock += 1
    for i in range(0, processes_amount-1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((general_address, processes_ports[i]))
        s.sendall(request)

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
                'type': "request",
                'clock': local_clock,
                'process_id': process_id
            }
            send_requests(request)
            item = [request["clock"], process_id, request]
            add_to_queue(item)
        time.sleep(2)
    
#################################################### MAIN ##################################################

if __name__ == "__main__":
    thread1 = threading.Thread(target=client)
    thread2 = threading.Thread(target=server)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

