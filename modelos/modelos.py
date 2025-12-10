# modelos/modelos.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Base para todos los modelos
Base = declarative_base()

# ==============================
# MODELO: USERS (datos API)
# ==============================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50))
    website = Column(String(255))

    # Relación: un usuario tiene muchos TODOs
    todos = relationship("Todo", back_populates="user")

    def __repr__(self):
        return f"<User id={self.id}, username='{self.username}'>"


# ==============================
# MODELO: TODOS (datos API)
# ==============================

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    completed = Column(Boolean, nullable=False)

    # Relación inversa
    user = relationship("User", back_populates="todos")

    def __repr__(self):
        estado = "✓" if self.completed else "✗"
        return f"<Todo id={self.id}, title='{self.title[:15]}...', completed={estado}>"


# ==============================
# MODELO: USUARIOS (login)
# ==============================

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    contrasena = Column(String(255), nullable=False)
    sal = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<Usuario username='{self.username}'>"