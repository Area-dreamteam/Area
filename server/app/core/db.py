from sqlmodel import create_engine, SQLModel



engine = create_engine(f"postgresql+psycopg2://root:root@pgdata:5432/area")



def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
