#pip install mysql-connector-python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from auxiliares import usuario_db, servidor_db, puerto_db, nombre_db

url_db = f"mysql+mysqlconnector://{usuario_db}:@{servidor_db}:{puerto_db}/{nombre_db}"

engine = create_engine(url_db, echo=False)
Session = sessionmaker(bind=engine)
session = Session()