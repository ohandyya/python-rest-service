from sqlalchemy import Column, Integer, String

from database.db import Base


class Activity(Base):
    __tablename__ = "activity"

    id = Column("id", type_=Integer, primary_key=True, index=True)
    name = Column("name", type_=String(64), unique=True)
    male_players = Column("male_players", type_=Integer)
    female_players = Column("female_players", type_=Integer)


class ActivityProbability(Base):
    __tablename__ = "activity_probability"

    id = Column("id", type_=Integer, primary_key=True, index=True)
    gender = Column("gender", type_=String, unique=True)
    probability = Column("probability", type_=String)
