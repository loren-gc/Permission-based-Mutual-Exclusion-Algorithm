# Permission-based Mutual Exclusion Algorithm  

This project implements a **distributed permission-based mutual exclusion algorithm**, following the Ricart & Agrawala approach.  
It ensures that only one process at a time can access a shared resource or enter the critical section in a distributed system.

---

## 📌 Project Specifications
- Implementation of the **Ricart & Agrawala** algorithm for distributed mutual exclusion.  
- Every request must **always be answered** (REQUEST → REPLY), regardless of whether access is immediately granted.  
- Assumption: there are **no process or channel failures** in the system.  
- Scenario with **3 independent processes**:
  - `process1.py`
  - `process2.py`
  - `process3.py`
- Multiple situations should be created to test and validate the correct behavior of the algorithm.  

---

## ⚙️ How It Works

Each process maintains a **Lamport logical clock** and communicates with the others through TCP sockets.  
When a process wants to access the shared resource, it sends a **request** in multicast to the other processes.  
When receiving a request, a process must reply to it in unicast, directly to the sender process.  
All requests are placed in a **priority queue**, ordered by the logical clock and the process id.  

The global variable `interest` tracks the current state of the process regarding the resource:
- `"no"` → not interested in the resource  
- `"yes"` → requesting access  
- `"using"` → currently inside the critical section  
- `"waiting"` → special state used to flag that more than one process is waiting for the resourceto be released  

Access to the critical section is granted only when the requesting process is at the head of the queue and has received replies from all other processes!!!.


---

## 📂 Project Structure

    Permission-based-Mutual-Exclusion-Algorithm/
    ├── process1.py
    ├── process2.py
    ├── process3.py
    └── README.md

---

## ▶️ How to Run
1. Clone this repository:
   ```bash
   git clone <https://github.com/loren-gc/Permission-based-Mutual-Exclusion-Algorithm>
   cd <Permission-based-Mutual-Exclusion-Algorithm>

2. **Open three different terminals**

3. **Run each process on its own terminal:**

```bash
# Terminal 1 - Process 0
python3 process1.py

# Terminal 2 - Process 1  
python3 process2.py

# Terminal 3 - Process 2
python3 process3.py


