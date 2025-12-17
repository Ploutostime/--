from db import engine, Base
import models

def create_all():
    Base.metadata.create_all(bind=engine)
    print("tables created")

if __name__ == "__main__":
    create_all()
