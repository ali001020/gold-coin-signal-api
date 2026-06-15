from core.database import engine, Base
from tasks import models

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")