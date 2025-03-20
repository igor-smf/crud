# Sistema de Controle de Movimentação de Estoque

Este projeto é uma API RESTful construída com FastAPI para o gerenciamento de movimentação de estoque de produtos. A aplicação permite o registro de movimentações de entrada e saída de produtos, com validação da quantidade disponível no estoque antes de permitir qualquer movimentação. O sistema foi projetado para garantir a integridade do estoque, permitindo operações seguras e eficientes de controle de inventário. Além disso, a API oferece endpoints claros e flexíveis para facilitar o gerenciamento de produtos e movimentações em qualquer sistema que precise dessa funcionalidade.

## Tecnologias Utilizadas

- **FastAPI**: Framework para construção de APIs rápidas e robustas.
- **PostgreSQL**: Banco de dados relacional utilizado para armazenar informações sobre produtos, movimentações de estoque e outros dados.
- **SQLAlchemy**: ORM para interação com o banco de dados PostgreSQL.
- **Pydantic**: Utilizado para validação e parsing de dados.
- **Streamlit**: Ferramenta para criar interfaces interativas e visuais diretamente em Python, utilizada para gerenciar produtos e movimentações.
- **Uvicorn**: Servidor ASGI utilizado para rodar a aplicação FastAPI.
- **Docker**: Para containerização da aplicação e garantir que o ambiente de desenvolvimento seja facilmente reproduzido.

## Funcionalidades

- **Cadastro de Produtos**: Permite cadastrar novos produtos com nome, descrição e preço.
- **Exibição de Produtos**: Visualização de todos os produtos cadastrados no sistema.
- **Detalhamento de Produto**: Consulta detalhada das informações de um produto específico pelo ID.
- **Atualização de Produto**: Atualização de informações como nome, descrição e preço de um produto.
- **Deleção de Produto**: Exclusão de um produto do sistema.
- **Movimentação de Estoque**: Registro de movimentações de estoque, tanto de entrada quanto de saída.
- **Consulta de Estoque**: Permite verificar a quantidade disponível de um produto no estoque.


## Como Rodar o Projeto com Docker Compose

### Passo 1: Criar as imagens e rodar os contêineres

Execute o seguinte comando para construir as imagens e iniciar os contêineres:

```bash
docker-compose up --build
```
### Passo 2: Acessar a API

Após o Docker Compose iniciar os contêineres, a API estará disponível em `http://localhost:8000`. Você pode acessar a documentação interativa da API pelo Swagger UI:

http://localhost:8000/docs


### Passo 3: Acessar a Interface de Usuário

A interface de usuário interativa estará disponível em:

http://localhost:8501