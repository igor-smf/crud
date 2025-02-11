"""
Importa a função create_engine do SQLAlchemy. 
Esta função é usada para criar uma conexão com o banco de dados especificado por uma URL.
"""
from sqlalchemy import create_engine

"""
Esta função declarative_base retorna uma classe base que será usada para declarar modelos de dados em Python. 
Ou seja, você definirá as classes que mapeiam para tabelas no banco de dados 
a partir dessa classe base.
"""
from sqlalchemy.ext.declarative import declarative_base

"""
Importa a função sessionmaker que é uma fábrica para criar sessões de banco de dados. 
Uma sessão permite executar comandos SQL e interagir com o banco.
"""
from sqlalchemy.orm import sessionmaker

"""
Esta é a URL de conexão com o banco de dados, especificando:
    postgresql: O sistema de banco de dados a ser usado (PostgreSQL).
    user: O nome do usuário para acessar o banco de dados.
    password: A senha para o usuário especificado.
    postgres: O host onde o banco de dados está rodando. No contexto de um Docker Compose, 
    isso seria o nome do serviço do PostgreSQL.
    mydatabase: O nome do banco de dados a ser acessado.
"""
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgres/mydatabase"

"""
Chama a função create_engine com a URL de conexão como argumento. 
O resultado é um objeto engine que mantém a conexão com o banco de dados especificado na URL. 
Este objeto será utilizado para interagir com o banco de dados, seja para executar consultas, 
atualizações ou deletar operações através de sessões geradas a partir dele.
"""
engine = create_engine(SQLALCHEMY_DATABASE_URL)

"""
Configura e cria uma fábrica de sessões de banco de dados. autocommit=False significa que 
é necessário chamar commit() manualmente para salvar transações no banco. autoflush=False 
evita que o SQLAlchemy envie automaticamente consultas SQL ao banco antes de chamar commit(). 
bind=engine associa esta fábrica de sessões à engine criada.
"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

"""
Base para os modelos declarativos
Base: Essa é a classe base para todas as classes que representarão 
as tabelas no banco de dados. 
Cada classe que você define, herdando de Base, será mapeada para uma tabela no banco de dados.
Ao herdar de Base, cada classe "declarativa" representa uma tabela, e os atributos da classe 
representam as colunas dessa tabela.
"""
Base = declarative_base()

def get_db():
    # Cria uma sessão de banco de dados local usando o objeto SessionLocal configurado
    db = SessionLocal()
    try:
        # Yield retorna a sessão db para ser usada em algum contexto
        yield db
    finally:
        # Garante que a sessão seja fechada após o uso, mesmo se ocorrerem erros
        db.close()