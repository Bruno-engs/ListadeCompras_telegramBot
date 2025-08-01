# Telegram Lista de Compras Bot

Este projeto é um bot para Telegram que auxilia no gerenciamento de ingredientes, receitas e listas de compras de forma interativa e fácil.  
Ideal para quem quer organizar compras de mercado, planejar receitas ou simplesmente manter controle dos itens em casa.

## Funcionalidades

- **Cadastro de ingredientes**  
  Adicione ingredientes com unidades restritas (kg, un, cx, g, ml) usando botões.

- **Cadastro de receitas**  
  Crie receitas informando nome e ingredientes já cadastrados.

- **Montagem de lista de compras**  
  Adicione ingredientes ou receitas à sua lista de compras e veja o resumo final.

- **Exclusão**  
  Exclua ingredientes ou receitas do sistema.

- **Menu interativo**  
  Todas as opções são apresentadas por botões, facilitando o uso.

## Estrutura do Projeto

```
telegramBot/
│
├── main.py
├── handlers/
│   ├── menu.py
│   ├── ingredientes.py
│   ├── receitas.py
│   ├── lista_compras.py
│   └── excluir.py
├── utils/
│   └── persistencia.py
├── data/
│   ├── ingredientes.json
│   └── receitas.json
└── requirements.txt
```

## Como usar

1. **Clone o repositório**
   ```
   git clone https://github.com/seu-usuario/seu-repo.git
   cd seu-repo/telegramBot
   ```

2. **Instale as dependências**
   ```
   pip install -r requirements.txt
   ```

3. **Configure o token do bot**
   - Edite o arquivo `main.py` e coloque o token do seu bot Telegram.

4. **Execute o bot**
   ```
   python main.py
   ```

## Observações

- Os dados são salvos em arquivos JSON na pasta `data/`.
- O bot foi desenvolvido para facilitar o uso por qualquer pessoa, sem necessidade de comandos complexos.
- Para dúvidas ou sugestões, abra uma issue no GitHub.

---
