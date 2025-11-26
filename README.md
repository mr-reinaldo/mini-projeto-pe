# mini-projeto-pe

Gerenciador de tarefas simples para terminal usando [Rich](https://github.com/Textualize/rich). As tarefas ficam guardadas localmente em `tarefas.pkl` no mesmo diretório do script.

## Funcionalidades
- Listar tarefas pendentes e concluídas.
- Adicionar tarefas com título e descrição.
- Marcar tarefas como concluídas.
- Remover tarefas que não são mais necessárias.

## Pré-requisitos
- Python 3.10+
- `pip` instalado

## Como rodar
1. Clone o repositório:
   ```bash
   git clone https://github.com/<seu-usuario>/mini-projeto-pe.git
   cd mini-projeto-pe
   ```
2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
3. Instale as dependências:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. Execute o aplicativo:
   ```bash
   python tasks.py
   ```
   O menu apresenta as opções:
   - `1` Listar tarefas
   - `2` Adicionar tarefa
   - `3` Concluir tarefa
   - `4` Remover tarefa
   - `0` Sair

## Capturas de tela
- Menu inicial  
  ![Menu](https://github.com/user-attachments/assets/666b7a70-71de-4c89-a7ae-b0ddea5208aa)
- Adicionando tarefa  
  ![Adicionar tarefa](https://github.com/user-attachments/assets/7a126a57-e3da-4131-a9ec-9500a3600f88)
- Listando tarefas  
  ![Listar tarefas](https://github.com/user-attachments/assets/8dc71961-883f-4f5a-89a8-e4011616ccaf)
- Concluindo tarefa  
  ![Concluir tarefa](https://github.com/user-attachments/assets/1a92d1dd-61b8-4c41-b9c9-114eedc73928)
- Tarefa concluída  
  ![Tarefa concluída](https://github.com/user-attachments/assets/1e923a66-0d42-44e5-b294-2005ac693ba8)
- Removendo tarefa  
  ![Remover tarefa](https://github.com/user-attachments/assets/5e96a5f8-aa2a-417d-af78-86f0a70e27b3)
- Saindo da aplicação  
  ![Sair](https://github.com/user-attachments/assets/48355622-1304-4211-9221-29501c44d0f1)
