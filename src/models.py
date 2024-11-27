import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, func, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(120), unique=True, nullable=False)
    email = Column(String(320), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    favorites = relationship('Favorites', back_populates='user')

    def __init__(self, user_name, email, password):
        self.user_name = user_name
        self.email = email
        self.password = password
        self.is_active = True
    def __repr__(self):
        return '<User %r>' % self.user_name

    def serialize(self, include_favorites=False):
        data = {
            "id": self.id,
            "user_name": self.user_name,
            "email": self.email,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_favorites:
            data["favorites"] = [favorite.serialize() for favorite in self.favorites]
        return data


class Planets(Base):
    __tablename__ = 'planets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), unique=False, nullable=False)
    terrain = Column(String(120), unique=False, nullable=False)
    climate = Column(String(120), unique=False, nullable=False)
    population = Column(Integer, unique=False, nullable=False)
    orbital_period = Column(Integer, nullable=True)
    diameter = Column(Integer, nullable=True)

    residents = relationship('People', back_populates='planet')
    favorites = relationship('Favorites', back_populates='planet')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "climate": self.climate,
            "population": self.population,
            "residents": [resident.serialize() for resident in self.residents],
        }


class People(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    gender = Column(Enum('male', 'female', 'n/a', name="gender_enum"), nullable=False)
    height = Column(Integer, nullable=False)
    hair_color = Column(String(120), nullable=False)
    skin_color = Column(String(120), nullable=False)
    birth_year = Column(String(120), nullable=True)
    homeworld_id = Column(Integer, ForeignKey('planets.id'))

    planet = relationship('Planets', back_populates='residents')
    favorites = relationship('Favorites', back_populates='people')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "height": self.height,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "homeworld": self.planet.serialize() if self.planet else None,
        }
class Favorites(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    planet_id = Column(Integer, ForeignKey('planets.id'))
    people_id = Column(Integer, ForeignKey('people.id'))
    created_at = Column(DateTime, default=func.now())

    user = relationship('User', back_populates='favorites')
    planet = relationship('Planets', back_populates='favorites')
    people = relationship('People', back_populates='favorites')
    

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet": self.planet.serialize() if self.planet else None,
            "people": self.people.serialize() if self.people else None,
        }

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
