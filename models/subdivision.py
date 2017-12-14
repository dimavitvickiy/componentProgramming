from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from config import DB_ENGINE, POSTGRESQL_ENGINE
from models import Base, session
from models.abstract import AbstractModel


class SubdivisionPostgres(Base, AbstractModel):
    __tablename__ = 'subdivisions'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    employee_list = relationship("EmployeePostgres", back_populates="subdivision",
                             cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f'<Subdivision(name={self.name})>'

    @classmethod
    def get_list(cls, *args, **kwargs):
        return session.query(cls).all()

    @classmethod
    def get_entity(cls, id_=None, name=None, *args, **kwargs):
        if not (id_ or name):
            raise AttributeError

        query = session.query(cls)
        if id_:
            query = query.filter_by(id=id_)
        if name:
            query = query.filter_by(name=name)
        return query.one_or_none()

    @classmethod
    def update(cls, id_, *args, name=None, **kwargs):
        subdivision = cls.get_entity(id_)
        subdivision.name = name or subdivision.name
        session.commit()
        return subdivision

    @classmethod
    def create(cls, name, *args, **kwargs):
        subdivision = cls(
            name=name,
        )
        session.add(subdivision)
        session.commit()
        return subdivision

    @classmethod
    def delete(cls, id_, *args, **kwargs):
        subdivision = cls.get_entity(id_)
        session.delete(subdivision)
        session.commit()


Subdivisions = {
    POSTGRESQL_ENGINE: SubdivisionPostgres,
}

Subdivision = Subdivisions[DB_ENGINE]
