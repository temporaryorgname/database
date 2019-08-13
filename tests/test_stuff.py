import pytest
import psycopg2

import tracker_database
from tracker_database import Food

@pytest.fixture()
def db_session():
    tracker_database.init_engine(tracker_database.get_db_uri())
    db_metadata = tracker_database.Base.metadata
    db_engine = tracker_database.engine
    db_metadata.create_all(bind=db_engine)
    yield tracker_database.Session
    db_metadata.drop_all(bind=db_engine)

@pytest.fixture()
def db_engine():
    tracker_database.init_engine(tracker_database.get_db_uri())
    return tracker_database.engine

@pytest.fixture()
def db_metadata():
    tracker_database.init_engine(tracker_database.get_db_uri())
    return tracker_database.Base.metadata

def test_init_db(db_session, db_engine):
    tables = db_engine.execute('SELECT * FROM pg_catalog.pg_tables')
    table_names = [t[1] for t in tables]
    print('Table names:', table_names)
    expected_table_names = ['food', 'photo', 'tag', 'photo_label', 'users', 'user_profile', 'body']
    for t in expected_table_names:
        assert t in table_names
