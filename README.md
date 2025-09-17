# Permission-based-Mutual-Exclusion-Algorithm  

Implementação de um algoritmo de exclusão mútua por permissão distribuída que garante que apenas um processo possa acessar um recurso ou a uma região crítica por vez em um sistema distribuído

---

## 📌 Especificações do Trabalho
- Implementação do algoritmo de Ricart & Agrawala para exclusão mútua por meio de permissão distribuída.  
- Cada requisição deve ser **sempre respondida** (REQUEST → REPLY), independentemente de conceder ou não o acesso imediato.  
- Considera-se que **não há falhas** de processos ou de canais de comunicação.  
- Cenário com **3 processos** independentes:
  - `process1.py`
  - `process2.py`
  - `process3.py`
- Diferentes situações devem ser criadas para testar e validar o funcionamento correto do algoritmo.

---

## 📂 Estrutura do Projeto:

    Permission-based-Mutual-Exclusion-Algorithm/
    ├── process1.py
    ├── process2.py
    ├── process3.py
    └── README.md


---

## ▶️ Como Executar
1. Clone este repositório:
   ```bash
   git clone <https://github.com/loren-gc/Permission-based-Mutual-Exclusion-Algorithm>
   cd <Permission-based-Mutual-Exclusion-Algorithm>

2. **Abra três terminais diferentes**

3. **Execute cada processo em um terminal separado:**

```bash
# Terminal 1 - Processo 0
python3 process1.py

# Terminal 2 - Processo 1  
python3 process2.py

# Terminal 3 - Processo 2
python3 process3.py


