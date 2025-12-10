from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50))
    website = Column(String(255))

    # Un usuario tiene muchos TODOS
    todos = relationship("Todo", back_populates="user")

    def __repr__(self):
        return f"<User id={self.id}, username='{self.username}'>"

class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    completed = Column(Boolean, nullable=False)

    # Relación inversa con User
    user = relationship("User", back_populates="todos")

    def __repr__(self):
        estado = "✓" if self.completed else "✗"
        return f"<Todo id={self.id}, title='{self.title[:15]}...', done={estado}>"