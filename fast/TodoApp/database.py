from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

SQL_ALCHEMY_URL ="sqlite:///./todoapp.db"
engine = create_engine(SQL_ALCHEMY_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind = engine)
base = declarative_base()