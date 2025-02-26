"""
Importa a classe FastAPI do módulo fastapi. Essa classe é usada para criar a 
aplicação web principal.
"""
from fastapi import FastAPI

"""
Importa a variável engine do módulo database. 
O engine é tipicamente usado para se conectar ao banco de dados. 
Ele serve como a interface principal para a base de dados e é usado para executar 
as instruções SQL.
"""
from database import engine

"""
Importa o módulo models. 
Este módulo geralmente contém definições de modelos de dados usando um ORM 
(Object-Relational Mapping), como SQLAlchemy, que mapeia classes Python a tabelas no 
banco de dados.
"""
import models
"""
Importa a variável router do módulo router. No FastAPI, router é usado para declarar 
operações de API diferentes, facilitando a organização e reutilização de código ao 
agrupar rotas relacionadas.
"""
from router import router

"""
Esta linha executa a criação das tabelas no banco de dados, baseadas nas 
definições de modelos encontradas no módulo models. 
O método create_all() verifica as tabelas definidas nos modelos e as cria no banco de dados, 
vinculado pelo engine, se ainda não existirem.
"""
models.Base.metadata.create_all(bind=engine)

"""
Cria uma instância da aplicação FastAPI. 
Esta instância será usada para registrar as rotas e iniciar o servidor.
"""
app = FastAPI()

"""
Inclui o roteador (definido em outra parte do código e importado) na aplicação. 
Isso efetivamente adiciona todas as rotas e operações definidas no router à aplicação 
FastAPI, permitindo que elas sejam acessadas via HTTP.
"""
app.include_router(router)