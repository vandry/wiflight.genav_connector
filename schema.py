#!/usr/bin/python

from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base

class Base(object):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }

Base = declarative_base(cls=Base)

class Resource(Base):
    """GenAV resources can be any combination of instructor and resource
    (resources being aircraft, sims, and classrooms which are listed in
    DataResources.

    So we cache both instructors and resources proper in this table.
    The only thing we ever care about is whether or not the thing is an
    aircraft, because if it's not then we ignore it altogether.

    Whenever we detect a ResourceID1 or ResourceID2 we don't recognize
    in a booking, we attempt to refresh the full contents of this table.
    New aircraft and instructors (or simulators) shouldn't occur that
    often, so a full reload of the table in that situation should not
    be too bad.
    """
    __tablename__ = 'resources'

    CompCode = Column(String(255), nullable=False, primary_key=True)
    ResourceID = Column(String(255), nullable=False, primary_key=True)
    resource_type = Column(Enum('instructor', 'aircraft', 'other'), nullable=False)

class LastUpdate(Base):
    """The date stamp of the latest entry we know about in the
    ActivityUpdates list. When we query again, we will ask for this
    timestamp forward.
    """
    __tablename__ = 'last_update'

    CompCode = Column(String(255), nullable=False, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    milliseconds = Column(Integer(unsigned=True), nullable=False)
