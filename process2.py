# Lorenzo Grippo Chiachio - 823917
# João Vitor Seiji - 822767

import socket
import threading
import queue
import json
import time

# local_clock:
#       INCREMENT WHEN SENDING MESSAGE OR ACK\NACK
#       INCREMENT ON THE OCCURRENCE OF EVENTS

#########################################################################################################

# process variables
process_id = 1
processes_ports = [5050, 5052]

################################################## from this line, the code is the same for all processes

lock = threading.Lock()

processes_amount = 3
local_clock = 0

general_address = "127.0.0.1"
server_ip = "127.0.0.1"
server_port = 5050+process_id

# global variable to keep track of the process interest on the resource ("yes", "no", "using" or "waiting")
interest = "no"
interest_queue = queue.PriorityQueue()
nack_counter = 0

###################################### FUNCTIONS AND PROCEDURES ##########################################

def add_to_queue(item):
    global interest_queue
    with lock:
        interest_queue.put(item)

def nack_to_next_in_line():
    if interest_queue.empty():
        return
    next_in_line = interest_queue.get()
    if next_in_line[2]["process_id"] == process_id:
        next_in_line = interest_queue.get()
    send_nack(general_address, next_in_line[2]["process_id"])

def use_resource():
    print("USING THE RESOURCE...")
    global interest
    with lock:
        interest = "using"
    time.sleep(10) #here, we SIMULATE the process using the resource
    print("RESOURCE RELEASED\n")
    with lock:
        interest = "no"
    nack_to_next_in_line()
    interest_queue.queue.clear() #emptying the priority queue

def inspect_queue():
    global interest
    if interest != "yes" or nack_counter < processes_amount-1:
        return
    queue_head = interest_queue.get()
    if queue_head[2]["process_id"] == process_id:
        use_resource()
        nack_to_next_in_line()
    else:
        with lock:
            interest = "waiting"

def send_mutual_request(destiny_address, destiny_process_id):
    mutual_request = {
        'type': "request",
        'clock': local_clock,
        'process_id': process_id
    }
    destiny_port = 5050 + destiny_process_id
    payload = json.dumps(mutual_request).encode("utf-8")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((destiny_address, destiny_port))
    s.sendall(payload)

def send_nack(destiny_address, destiny_process_id):
    global local_clock
    with lock:
        local_clock += 1
    nack = {
        "type": "nack",
        "clock": local_clock,
        "process_id": process_id
    }
    destiny_port = 5050 + destiny_process_id
    payload = json.dumps(nack).encode("utf-8") 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((destiny_address, destiny_port))
    s.sendall(payload)

def handle_request(request):
    global interest
    if interest == "no":
        send_nack(general_address, request["process_id"])
    elif interest == "using":
        item = [request["clock"], request["process_id"], request]
        add_to_queue(item)
    elif interest == "yes":
        global nack_counter
        nack_counter+=1
        item = [request["clock"], request["process_id"], request]
        add_to_queue(item)
        interest = "waiting"
        send_mutual_request(general_address, request["process_id"])

def handle_nack():
    global nack_counter
    with lock:
        nack_counter += 1
    if interest == "waiting":
        use_resource()
        nack_to_next_in_line()

def handle_message(message): #it can be either a request or a nackd
    if message["type"] == "request":
        handle_request(message)
    else:
        handle_nack()
    inspect_queue()

def clock_maintenance(foreign_clock):
    global local_clock
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

def send_requests(request):
    global local_clock
    with lock:
        local_clock += 1
    payload = json.dumps(request).encode("utf-8")
    for i in range(0, processes_amount-1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((general_address, processes_ports[i]))
        s.sendall(payload)

def wait_answers():
    global nack_counter
    while nack_counter < processes_amount-1 or interest != "no":
        continue
    with lock:
        nack_counter = 0

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
                'type': "request",
                'clock': local_clock,
                'process_id': process_id
            }
            send_requests(request)
            item = [request["clock"], process_id, request]
            add_to_queue(item)
            wait_answers()
        time.sleep(1)
    
#################################################### MAIN ##################################################

if __name__ == "__main__":
    thread1 = threading.Thread(target=client)
    thread2 = threading.Thread(target=server)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

