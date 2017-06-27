from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

dec_base = declarative_base()


class DPerson(dec_base):
    """Create people table"""
    __tablename__ = 'person'
    person_id = Column(Integer, primary_key=True,
                       nullable=False, autoincrement=True)
    person_number = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    person_type = Column(String, nullable=False)


class DRoom(dec_base):
    """Create the rooms table"""
    __tablename__ = 'room'
    room_id = Column(Integer, primary_key=True, autoincrement=True)
    room_name = Column(String(32), nullable=False)
    room_type = Column(String(32), nullable=False)
    capacity = Column(Integer, nullable=False)


class OfficeAllocations(dec_base):
    """Create the rooms table"""
    __tablename__ = 'tb_office_allocations'
    allocation_id = Column(Integer, primary_key=True, autoincrement=True)
    room_name = Column(String(32), nullable=False)
    members = Column(String(255))
    member_ids = Column(String(255))


class LivingSpaceAllocations(dec_base):
    """Create the rooms table"""
    __tablename__ = 'tb_living_space_allocations'
    allocation_id = Column(Integer, primary_key=True, autoincrement=True)
    room_name = Column(String(32), nullable=False)
    members = Column(String(255))
    member_ids = Column(String(255))


class DatabaseBuilder(object):
    """assigns database name and creates a session"""
    def __init__(self, db_name="my_default_db"):
        self.db_name = db_name
        self.engine = create_engine('sqlite:///' + self.db_name + ".sqlite")
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)
        dec_base.metadata.create_all(self.engine)
