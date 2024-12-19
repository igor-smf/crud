from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Essa URL instrui o SQLAlchemy sobre onde e como se conectar ao banco de dados PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgres/mydatabase"

# Cria o motor do banco de dados, é que o conecta com o banco
# Este motor não abre uma conexão imediatamente, mas configura tudo para que o código possa solicitar conexões conforme necessário.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Sessão de banco de dados, é quem vai executar as queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos declarativos
# Base: Essa é a classe base para todas as classes que representarão as tabelas no banco de dados. Cada classe que você define, herdando de Base, será mapeada para uma tabela no banco de dados.
# Ao herdar de Base, cada classe "declarativa" representa uma tabela, e os atributos da classe representam as colunas dessa tabela.
Base = declarative_base() # ORM


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()