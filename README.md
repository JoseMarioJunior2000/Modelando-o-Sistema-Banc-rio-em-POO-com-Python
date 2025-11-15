# Desafio – Banco Digital Orientado a Objetos (Trilha Python DIO)

Atualização do sistema bancário para utilizar **Programação Orientada a Objetos (POO)**, conforme o modelo UML proposto na trilha Python da DIO.  
Os dados de clientes e contas agora são armazenados em **objetos**, e as operações são representadas por **classes de transação**.

---

## 📘 Objetivo
Implementar um sistema bancário com:
- Armazenamento de dados em **objetos** (sem dicionários);
- **Histórico** de transações em cada conta;
- Classes baseadas em **herança** e **abstração**;
- **Limite de saque** e **limite de quantidade de saques** na conta corrente.

---

## 🧱 Estrutura de Classes (UML simplificado)

```
┌────────────────────────┐
│        Historico        │
│ + adicionar_transacao() │
└────────────┬────────────┘
             │1
             │
             ▼
┌────────────────────────┐
│         Conta           │
│ - saldo                 │
│ - numero                │
│ - agencia               │
│ - cliente               │
│ - historico             │
│ + sacar()               │
│ + depositar()           │
│ + nova_conta()          │
└────────────┬────────────┘
             │
             ▼
┌────────────────────────┐
│     ContaCorrente       │
│ - limite                │
│ - limite_saques         │
│ + sacar()               │
└────────────────────────┘

┌────────────────────────┐
│       Transacao (ABC)   │
│ + registrar(conta)      │
└────────────┬────────────┘
             │
   ┌─────────┴──────────┐
   │                    │
┌──────────────┐   ┌───────────┐
│   Deposito    │   │   Saque   │
└──────────────┘   └───────────┘

┌────────────────────────┐
│        Cliente          │
│ - endereco              │
│ - contas (list)         │
│ + adicionar_conta()     │
│ + realizar_transacao()  │
└────────────┬────────────┘
             │
             ▼
┌────────────────────────┐
│     PessoaFisica        │
│ - cpf                   │
│ - nome                  │
│ - data_nascimento        │
└────────────────────────┘
```

---

## 🧭 Funcionalidades
- Criar cliente (CPF único);
- Criar conta corrente vinculada a um cliente;
- Realizar depósitos e saques;
- Exibir extrato detalhado com data e hora das operações;
- Listar todas as contas registradas;
- Limitar saques por **valor máximo (R$ 500)** e **quantidade (3 por dia)**.

---

## ▶️ Como executar
1. Salve o código em `main.py`.
2. Execute no terminal:
   ```bash
   python main.py
   ```
3. Utilize o menu interativo.

---

## 📜 Menu
```
[d] Depositar
[s] Sacar
[e] Extrato
[u] Criar cliente
[n] Criar conta corrente
[l] Listar contas
[q] Sair
```

---

## 📂 Estrutura de dados em memória
Os objetos são criados e armazenados dinamicamente:

```python
PessoaFisica(cpf="12345678900", nome="Maria", data_nascimento=date(1990,1,1), endereco="Rua A, 100 - Centro - SP")

ContaCorrente(cliente=maria, numero=1, agencia="0001", limite=500, limite_saques=3)
```

Cada conta possui um `Historico` com transações do tipo `Deposito` ou `Saque`.

---

## 🧠 Regras principais
- **Saque:** valor positivo, <= saldo, <= limite, e até 3 saques por dia.
- **Depósito:** valor positivo.
- **Conta:** número sequencial, agência fixa `0001`.
- **Cliente:** não pode ter CPF duplicado.
- **Transações:** registradas automaticamente no histórico da conta.

---

## 🧩 Estrutura de arquivos
```
.
├── main.py        # Código principal com classes e menu
└── README.md      # Este arquivo
```

---

## 🧪 Exemplo de uso
```
[u] Criar cliente
Nome: João Silva
CPF: 123.456.789-00
Data de nascimento: 01/01/1990
Endereço: Rua A, 100 - Centro - São Paulo/SP

[n] Criar conta corrente
CPF do titular: 123.456.789-00

[d] Depositar
CPF do titular: 123.456.789-00
Valor: 300

[s] Sacar
CPF do titular: 123.456.789-00
Valor: 100

[e] Extrato
=========== EXTRATO ===========
01/11/2025 10:00:00 - Deposito: R$ 300.00
01/11/2025 10:05:00 - Saque: R$ 100.00
Saldo: R$ 200.00
================================
```

---

## 📝 Licença
Uso educacional – livre adaptação para estudo na trilha Python da **Digital Innovation One (DIO)**.
