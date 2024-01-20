import json
import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session

# Define a model
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    username = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    password = Column(String(50), nullable=False)

class Institute(Base):
    __tablename__ = 'institute'
    name = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    city = Column(String(50))
    state = Column(String(20))
    course1 = Column(String(50))
    course2 = Column(String(50))

# Create an SQLite in-memory database for testing purposes
DATABASE_URL = "sqlite:///./in.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Dependency function to get a database session
def get_db():
    db = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return db()

app = FastAPI()

@app.get("/example")
async def read_item(city: str, db: Session = Depends(get_db)):
    query_result = db.query(Institute).filter(Institute.city == city).all()
    return query_result

if __name__ == "__main__":
   uvicorn.run("m:app", host="127.0.0.1", port=8221, reload=True)
