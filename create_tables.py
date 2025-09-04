# create_tables.py
from database import Base, engine
from models import Item, Category

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    init_db()
