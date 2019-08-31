import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, Float, Date, Time, DateTime, Boolean, Enum

import enum
import datetime
import os

Base = declarative_base()
def set_base(base):
    global Base
    Base = base

def get_db_uri(config=None):
    if 'LOGS_DB_URI' in os.environ:
        return os.environ['LOGS_DB_URI']
    elif config is not None:
        return 'postgresql://{user}:{password}@{host}:{port}/{dbname}'.format(**config)
    else:
        return 'postgresql://howardh:verysecurepassword@localhost:5432/howardh'

engine = None
Session = None
def init_engine(db_uri, pool_size=10, max_overflow=20):
    global engine, Session
    if engine is None:
        print('Initialized DB at %s' % db_uri)
        engine = create_engine(db_uri, pool_size=pool_size, max_overflow=max_overflow)
        if engine is None:
            raise Exception('Failed to initalize engine at %s' % db_uri)
        Session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
        if Session is None:
            raise Exception('Failed to create Session factory.')
        Base.metadata.bind = engine
    return engine

def get_session(db_uri, pool_size=10, max_overflow=20):
    engine = init_engine()
    #Base.query = db_session.query_property()
    return Session

def cast_none(val, t):
    if val is None:
        return None
    try:
        return t(val)
    except:
        print('Could not convert "%s" of type %s to %s' % (val, type(val), t))
        return None

class Food(Base):
    __tablename__ = 'food'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    date = Column(Date)
    time = Column(Time)

    name = Column(String)
    quantity = Column(String)
    calories = Column(Float)
    protein = Column(Float)

    parent_id = Column(Integer)

    premade = Column(Boolean)
    finished = Column(Boolean)
    copied_from = Column(Integer)
    autogenerated = Column(Boolean)

    def to_dict(self):
        # Return as dictionary
        return {
            "id": self.id, 
            "date": str(self.date),
            "time": cast_none(self.time, str),
            "name": self.name, 
            "quantity": self.quantity,
            "calories": self.calories,
            "protein": self.protein,
            "parent_id": self.parent_id,
            "premade": self.premade,
            "finished": self.finished,
            "copied_from": self.copied_from,
            "autogenerated": self.autogenerated
        }

    @classmethod
    def from_dict(cls, data):
        f = cls()
        f.update_from_dict(data)
        return f

    def update_from_dict(self, data):
        if 'name' in data:
            self.name = data['name']
        if 'date' in data:
            self.date = data['date']
            if data['date'] is not None:
                y,m,d = data['date'].split('-')
                data['date'] = datetime.date(int(y), int(m), int(d))
        else:
            self.date = datetime.datetime.now()
        if 'time' in data and data['time'] != '':
            self.time = data['time']
        if 'quantity' in data:
            self.quantity = data['quantity']
        if 'calories' in data:
            self.calories = cast_none(data['calories'], float)
        if 'protein' in data:
            self.protein = cast_none(data['protein'], float)

        if 'parent_id' in data:
            self.parent_id = data['parent_id']

        if 'premade' in data:
            self.premade = data['premade']
        if 'finished' in data:
            self.finished = data['finished']
        if 'copied_from' in data:
            self.copied_from = data['copied_from']
        if 'autogenerated' in data:
            self.autogenerated = data['autogenerated']

    def validate(self):
        return True

class Photo(Base):
    __tablename__ = 'photo'
    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    user_id = Column(Integer)
    date = Column(Date)
    time = Column(Time)
    upload_time = Column(DateTime)
    food_id = Column(Integer)

    def to_dict(self):
        return {
            "id": self.id, 
            "user_id": self.user_id,
            "date": cast_none(self.date, str),
            "time": cast_none(self.time, str),
            "food_id": cast_none(self.food_id, int)
        }

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    parent_id = Column(Integer)
    tag = Column(String)
    description = Column(String)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'parent_id': self.parent_id,
            'tag': self.tag,
            'description': self.description
        }

    @classmethod
    def from_dict(cls, data):
        f = cls()
        f.update_from_dict(data)
        return f

    def update_from_dict(self, data):
        if 'parent_id' in data:
            self.parent_id = data['parent_id']
        if 'user_id' in data:
            self.user_id = data['user_id']
        if 'tag' in data:
            self.tag = data['tag']
        if 'description' in data:
            self.description = data['description']

    def validate(self):
        if self.tag is None:
            raise ValueError("No tag name provided.")
        if len(self.tag) == 0:
            raise ValueError("Invalid tag name.")

class PhotoLabel(Base):
    __tablename__ = 'photo_label'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    photo_id = Column(Integer)
    tag_id = Column(Integer)
    #bounding_box = Column(BOX)
    #bounding_polygon = Column(POLYGON)

    def to_dict(self):
        return {
            'id': l.id,
            'tag_id': l.tag_id,
            'bounding_box': l.bounding_box,
            'bounding_polygon': l.bounding_polygon
        }

    @classmethod
    def from_dict(cls, data):
        f = cls()
        f.update_from_dict(data)
        return f

    def update_from_dict(self, data):
        if 'user_id' in data:
            self.user_id = data['user_id']
        if 'photo_id' in data:
            self.photo_id = data['photo_id']
        if 'tag_id' in data:
            self.tag_id = data['tag_id']
        if 'bounding_box' in data:
            label.bounding_box = data['bounding_box']
        if 'bounding_polygon' in data:
            label.bounding_polygon = data['bounding_polygon']

    def validate(self):
        if self.tag_id is None:
            raise ValueError("No tag ID provided.")
        if self.photo_id is None:
            raise ValueError("No photo ID provided.")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    verified_email = Column(Boolean)

    active = False
    authenticated = False

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

class GenderEnum(enum.Enum):
    male = 1
    female = 2
    other = 3

WeightUnitsEnum = enum.Enum(
        value='WeightUnitsEnum',
        names=[
            ('kgs',1),
            ('kg',1),
            ('metric',1),
            ('lbs',2),
            ('lb',2),
            ('imperial',2)
        ]
)

class UserProfile(Base):
    __tablename__ = 'user_profile'
    id = Column(Integer, primary_key=True)
    display_name = Column(String)
    last_activity = Column(DateTime)
    gender = Column(Enum(GenderEnum))

    prefered_units = Column(Enum(WeightUnitsEnum))

    target_weight = Column(Float)
    target_calories = Column(Float)
    weight_goal = Column(String)

    country = Column(String)
    state = Column(String)
    city = Column(String)

    active = False
    authenticated = False

    @classmethod
    def from_dict(cls, data):
        f = cls()
        f.update_from_dict(data)
        return f

    def update_from_dict(self, data):
        if 'display_name' in data:
            self.display_name = data['display_name']
        if 'prefered_units' in data:
            self.prefered_units = data['prefered_units']
        if 'target_weight' in data:
            self.target_weight = data['target_weight']
        if 'target_calories' in data:
            self.target_calories = data['target_calories']
        if 'weight_goal' in data:
            self.weight_goal = data['weight_goal']
        if 'country' in data:
            self.country = data['country']
        if 'state' in data:
            self.state = data['state']
        if 'city' in data:
            self.city = data['city']

    def validate(self):
        if self.display_name is None:
            raise ValueError("No name provided.")
        if len(self.display_name) == 0:
            raise ValueError("Invalid name.")
        if self.target_weight is not None:
            try:
                float(self.target_weight)
            except:
                raise ValueError("Invalid target weight")
        if self.target_calories is not None:
            try:
                float(self.target_calories)
            except:
                raise ValueError("Invalid target Calories")

class Bodyweight(Base):
    __tablename__ = 'body'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    date = Column(Date)
    time = Column(Time)
    bodyweight = Column(Float)

    def to_dict(self):
        return {
            "id": self.id, 
            "user_id": self.user_id,
            "date": cast_none(self.date, str),
            "time": cast_none(self.time, str),
            "bodyweight": cast_none(self.bodyweight, float)
        }

class ComputedData(Base):
    __tablename__ = 'computed_data'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    last_updated = Column(DateTime)
    key = Column(String)
    value = Column(sqlalchemy.types.PickleType)
