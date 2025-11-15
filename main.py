from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional

class Historico:
    """Mantém o histórico de transações de uma conta."""
    def __init__(self) -> None:
        self._transacoes: List[dict] = []

    def adicionar_transacao(self, transacao: "Transacao") -> None:
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now(),
            }
        )

    @property
    def transacoes(self) -> List[dict]:
        return self._transacoes.copy()

    def contar_saques(self) -> int:
        return sum(1 for t in self._transacoes if t["tipo"] == "Saque")

    def __str__(self) -> str:
        if not self._transacoes:
            return "Não foram realizadas movimentações."
        linhas = []
        for t in self._transacoes:
            linhas.append(
                f"{t['data'].strftime('%d/%m/%Y %H:%M:%S')} - {t['tipo']}: R$ {t['valor']:.2f}"
            )
        return "\n".join(linhas)


class Transacao(ABC):
    """Interface de transação: deve registrar em uma conta."""
    def __init__(self, valor: float) -> None:
        self.valor = float(valor)

    @abstractmethod
    def registrar(self, conta: "Conta") -> bool:
        """Executa a transação na conta e retorna True/False para sucesso."""
        raise NotImplementedError


class Deposito(Transacao):
    def registrar(self, conta: "Conta") -> bool:
        ok = conta.depositar(self.valor)
        if ok:
            conta.historico.adicionar_transacao(self)
        return ok


class Saque(Transacao):
    def registrar(self, conta: "Conta") -> bool:
        ok = conta.sacar(self.valor)
        if ok:
            conta.historico.adicionar_transacao(self)
        return ok


class Cliente:
    def __init__(self, endereco: str) -> None:
        self.endereco = endereco
        self.contas: List[Conta] = []

    def realizar_transacao(self, conta: "Conta", transacao: Transacao) -> bool:
        if conta not in self.contas:
            print("Operação falhou! Conta não pertence a este cliente.")
            return False
        return transacao.registrar(conta)

    def adicionar_conta(self, conta: "Conta") -> None:
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento: date, endereco: str) -> None:
        super().__init__(endereco=endereco)
        self.cpf = "".join(filter(str.isdigit, cpf))
        self.nome = nome
        self.data_nascimento = data_nascimento


@dataclass
class Conta:
    cliente: Cliente
    numero: int
    agencia: str = "0001"
    _saldo: float = 0.0
    historico: Historico = field(default_factory=Historico)

    _sequencial: int = 0

    @property
    def saldo(self) -> float:
        return self._saldo

    @classmethod
    def nova_conta(cls, cliente: Cliente) -> "Conta":
        cls._sequencial += 1
        return cls(cliente=cliente, numero=cls._sequencial)

    def sacar(self, valor: float) -> bool:
        valor = float(valor)
        if valor <= 0:
            print("Operação falhou! Valor inválido.")
            return False
        if valor > self._saldo:
            print("Operação falhou! Saldo insuficiente.")
            return False
        self._saldo -= valor
        return True

    def depositar(self, valor: float) -> bool:
        valor = float(valor)
        if valor <= 0:
            print("Operação falhou! Valor inválido.")
            return False
        self._saldo += valor
        return True


@dataclass
class ContaCorrente(Conta):
    limite: float = 500.0
    limite_saques: int = 3

    def sacar(self, valor: float) -> bool:
        if self.historico.contar_saques() >= self.limite_saques:
            print("Operação falhou! Limite de saques diários atingido.")
            return False
        if valor > self.limite:
            print("Operação falhou! Valor excede o limite por saque.")
            return False
        return super().sacar(valor)

class BancoMemoria:
    def __init__(self) -> None:
        self._clientes: List[PessoaFisica] = []

    # Clientes
    def obter_cliente_por_cpf(self, cpf: str) -> Optional[PessoaFisica]:
        cpf = "".join(filter(str.isdigit, cpf))
        for c in self._clientes:
            if c.cpf == cpf:
                return c
        return None

    def criar_cliente(self, *, nome: str, cpf: str, data_nascimento: str, endereco: str) -> bool:
        if self.obter_cliente_por_cpf(cpf):
            print("Já existe cliente com este CPF.")
            return False
        try:
            dia, mes, ano = map(int, data_nascimento.split("/"))
            dn = date(ano, mes, dia)
        except Exception:
            print("Data de nascimento inválida. Use dd/mm/aaaa.")
            return False
        cliente = PessoaFisica(cpf=cpf, nome=nome, data_nascimento=dn, endereco=endereco)
        self._clientes.append(cliente)
        print("✅ Cliente criado com sucesso!")
        return True

    # Contas
    def criar_conta_corrente(self, cpf: str) -> Optional[ContaCorrente]:
        cliente = self.obter_cliente_por_cpf(cpf)
        if not cliente:
            print("Cliente não encontrado.")
            return None
        conta = ContaCorrente.nova_conta(cliente)
        cliente.adicionar_conta(conta)
        print(f"✅ Conta criada! Agência {conta.agencia} • Número {conta.numero}")
        return conta

    def listar_contas(self) -> None:
        tem = False
        for cli in self._clientes:
            for c in cli.contas:
                tem = True
                print(
                    f"Agência: {c.agencia} | Número: {c.numero} | Titular: {cli.nome} (CPF: {cli.cpf}) | Saldo: R$ {c.saldo:.2f}"
                )
        if not tem:
            print("Nenhuma conta cadastrada.")

# ============================
# Interface de linha de comando
# ============================

def main() -> None:
    banco = BancoMemoria()

    menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[u] Criar cliente
[n] Criar conta corrente
[l] Listar contas
[q] Sair
=> """

    while True:
        opcao = input(menu).strip().lower()

        if opcao == "u":
            nome = input("Nome: ")
            cpf = input("CPF: ")
            dn = input("Data de nascimento (dd/mm/aaaa): ")
            end = input("Endereço (logradouro, nro - bairro - cidade/UF): ")
            banco.criar_cliente(nome=nome, cpf=cpf, data_nascimento=dn, endereco=end)

        elif opcao == "n":
            cpf = input("CPF do titular: ")
            banco.criar_conta_corrente(cpf)

        elif opcao == "l":
            banco.listar_contas()

        elif opcao == "d":
            cpf = input("CPF do titular: ")
            cliente = banco.obter_cliente_por_cpf(cpf)
            if not cliente or not cliente.contas:
                print("Cliente/conta não encontrado(a).")
                continue
            conta = cliente.contas[0]
            valor = float(input("Valor do depósito: "))
            cliente.realizar_transacao(conta, Deposito(valor))

        elif opcao == "s":
            cpf = input("CPF do titular: ")
            cliente = banco.obter_cliente_por_cpf(cpf)
            if not cliente or not cliente.contas:
                print("Cliente/conta não encontrado(a).")
                continue
            conta = cliente.contas[0]
            valor = float(input("Valor do saque: "))
            cliente.realizar_transacao(conta, Saque(valor))

        elif opcao == "e":
            cpf = input("CPF do titular: ")
            cliente = banco.obter_cliente_por_cpf(cpf)
            if not cliente or not cliente.contas:
                print("Cliente/conta não encontrado(a).")
                continue
            conta = cliente.contas[0]
            print("\n=========== EXTRATO ===========")
            print(str(conta.historico))
            print(f"\nSaldo: R$ {conta.saldo:.2f}")
            print("================================")

        elif opcao == "q":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()