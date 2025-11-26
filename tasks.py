import os
import pickle
from pathlib import Path
from typing import List

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

# Caminho do arquivo de dados (fica ao lado deste script).
ARQUIVO_TAREFAS = Path(__file__).with_name("tarefas.pkl")

# Status são strings para facilitar salvamento/leitura.
STATUS_PENDENTE = "pendente"
STATUS_CONCLUIDA = "concluida"

# Instância global do console Rich.
console = Console()


class Tarefa:
    """Representa uma tarefa salva em disco."""

    def __init__(
        self,
        titulo: str,
        descricao: str,
        status: str = STATUS_PENDENTE,
    ) -> None:
        self.titulo = titulo
        self.descricao = descricao
        self.status = status

    def concluir(self) -> None:
        """Marca a tarefa como concluída."""
        self.status = STATUS_CONCLUIDA

    def para_dict(self) -> dict:
        """Converte para um dicionário simples (pickle-friendly)."""
        return {
            "titulo": self.titulo,
            "descricao": self.descricao,
            "status": self.status,
        }

    @classmethod
    def de_dict(cls, dados: dict) -> "Tarefa":
        """Cria a tarefa a partir de um dicionário salvo."""
        status = str(dados.get("status", STATUS_PENDENTE)).lower()
        status_normalizado = STATUS_CONCLUIDA if "conclu" in status else STATUS_PENDENTE
        return cls(
            titulo=dados.get("titulo", "").strip(),
            descricao=dados.get("descricao", "").strip(),
            status=status_normalizado,
        )


def limpar_tela() -> None:
    """Limpa a tela do terminal."""
    os.system("cls" if os.name == "Windows" else "clear")


def pausar() -> None:
    """Espera o usuário antes de voltar ao menu."""
    input("\nPressione Enter para voltar ao menu...")


def salvar_tarefas(tarefas: List[Tarefa]) -> None:
    """Grava a lista de tarefas em disco."""
    ARQUIVO_TAREFAS.parent.mkdir(parents=True, exist_ok=True)
    with ARQUIVO_TAREFAS.open("wb") as arquivo:
        pickle.dump([tarefa.para_dict() for tarefa in tarefas], arquivo)


def carregar_tarefas() -> List[Tarefa]:
    """Lê as tarefas já salvas, se existirem."""
    if not ARQUIVO_TAREFAS.exists():
        return []

    try:
        with ARQUIVO_TAREFAS.open("rb") as arquivo:
            dados = pickle.load(arquivo)
    except Exception:
        # Se o arquivo estiver corrompido, começamos com lista vazia.
        return []

    return [Tarefa.de_dict(item) for item in dados if isinstance(item, dict)]


def exibir_menu() -> str:
    """Mostra o menu principal e devolve a escolha do usuário."""
    console.print(Panel.fit("[bold cyan]GERENCIADOR DE TAREFAS[/bold cyan]"))
    console.print("[1] Listar tarefas")
    console.print("[2] Adicionar tarefa")
    console.print("[3] Concluir tarefa")
    console.print("[4] Remover tarefa")
    console.print("[0] Sair")
    return Prompt.ask("Opção", choices=["0", "1", "2", "3", "4"])


def exibir_tarefas(tarefas: List[Tarefa]) -> None:
    """Mostra a lista de tarefas em uma tabela colorida."""
    if not tarefas:
        console.print("[yellow]Nenhuma tarefa encontrada.[/yellow]")
        return

    tabela = Table(title="Lista de Tarefas", show_lines=True)
    tabela.add_column("ID", style="cyan", justify="center", no_wrap=True)
    tabela.add_column("Título", style="bold")
    tabela.add_column("Descrição", style="dim")
    tabela.add_column("Status", justify="center")

    for i, tarefa in enumerate(tarefas, start=1):
        status = (
            "[green]✔ Concluída[/green]"
            if tarefa.status == STATUS_CONCLUIDA
            else "[yellow]⏳ Pendente[/yellow]"
        )
        tabela.add_row(str(i), tarefa.titulo, tarefa.descricao, status)

    console.print(tabela)


def obter_dados_tarefa() -> dict:
    """Pergunta título e descrição para uma nova tarefa."""
    titulo = Prompt.ask("Título").strip()
    descricao = Prompt.ask("Descrição").strip()
    return {"titulo": titulo, "descricao": descricao}


def obter_indice(tarefas: List[Tarefa], acao: str) -> int:
    """Pede um ID válido da lista de tarefas."""
    if not tarefas:
        console.print("[yellow]Nenhuma tarefa disponível.[/yellow]")
        return -1

    try:
        indice = int(Prompt.ask(f"ID da tarefa para {acao}"))
    except ValueError:
        console.print("[red]Digite um número válido.[/red]")
        return -1

    if 1 <= indice <= len(tarefas):
        return indice - 1

    console.print("[red]ID inválido.[/red]")
    return -1


def adicionar_tarefa(tarefas: List[Tarefa]) -> None:
    dados = obter_dados_tarefa()
    if not dados["titulo"]:
        console.print("[red]O título não pode ficar vazio.[/red]")
        return

    tarefas.append(Tarefa(**dados))
    salvar_tarefas(tarefas)
    console.print("[green]Tarefa adicionada![/green]")


def concluir_tarefa(tarefas: List[Tarefa]) -> None:
    exibir_tarefas(tarefas)
    indice = obter_indice(tarefas, "concluir")
    if indice < 0:
        return

    tarefa = tarefas[indice]
    if tarefa.status == STATUS_CONCLUIDA:
        console.print("[yellow]Essa tarefa já está concluída.[/yellow]")
        return

    tarefa.concluir()
    salvar_tarefas(tarefas)
    console.print("[green]Tarefa concluída![/green]")


def remover_tarefa(tarefas: List[Tarefa]) -> None:
    exibir_tarefas(tarefas)
    indice = obter_indice(tarefas, "remover")
    if indice < 0:
        return

    tarefa = tarefas[indice]
    if Confirm.ask(f"Remover '{tarefa.titulo}'?"):
        tarefas.pop(indice)
        salvar_tarefas(tarefas)
        console.print("[green]Tarefa removida![/green]")


def principal() -> None:
    tarefas = carregar_tarefas()
    while True:
        limpar_tela()
        console.print(
            Panel.fit(
                "[bold green]Bem-vindo ao seu gerenciador de tarefas![/bold green]"
            )
        )
        opcao = exibir_menu()

        if opcao == "0":
            console.print("\n[cyan]Até logo![/cyan]\n")
            break
        if opcao == "1":
            limpar_tela()
            exibir_tarefas(tarefas)
            pausar()
        elif opcao == "2":
            limpar_tela()
            adicionar_tarefa(tarefas)
            pausar()
        elif opcao == "3":
            limpar_tela()
            concluir_tarefa(tarefas)
            pausar()
        elif opcao == "4":
            limpar_tela()
            remover_tarefa(tarefas)
            pausar()


if __name__ == "__main__":
    principal()
