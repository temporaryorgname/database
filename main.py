from tracker_database import init_db, Base, Food

#db_session = init_db('sqlite://', create_tables=True)
#db_session = init_db('sqlite:///:memory:', create_tables=True)

db_session = init_db('', create_tables=True)
print(Base.metadata.reflect())
print(Base.metadata.tables)
