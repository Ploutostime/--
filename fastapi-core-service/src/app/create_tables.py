from src.app.db import engine, Base
import src.app.models as models

def create_all():
    Base.metadata.create_all(bind=engine)
    print("tables created")

if __name__ == "__main__":
    create_all()
