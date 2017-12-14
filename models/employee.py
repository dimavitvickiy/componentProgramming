import six as six
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from config import DB_ENGINE, POSTGRESQL_ENGINE
from models import Base, session
from models.abstract import AbstractModel


class EmployeePostgres(Base, AbstractModel):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    subdivision_id = Column(Integer, ForeignKey('subdivisions.id'))
    subdivision = relationship("SubdivisionPostgres", back_populates="employee_list")

    def __repr__(self):
        return f'<Employee(first_name={self.first_name}, last_name={self.last_name})>'

    @classmethod
    def get_list(cls, *args, **kwargs):
        return session.query(cls).all()

    @classmethod
    def get_entity(cls, employee_id, *args, **kwargs):
        return session.query(cls).filter_by(id=employee_id).one_or_none()

    @classmethod
    def update(cls, employee_id, *args, first_name=None, last_name=None, subdivision=None, **kwargs):
        employee = cls.get_entity(employee_id)
        employee.first_name = first_name or employee.first_name
        employee.last_name = last_name or employee.last_name
        employee.subdivision = subdivision or employee.subdivision
        session.commit()
        return employee

    @classmethod
    def create(cls, first_name, last_name, subdivision, *args, **kwargs):
        employee = cls(
            first_name=first_name,
            last_name=last_name,
            subdivision=subdivision
        )
        session.add(employee)
        session.commit()
        return employee

    @classmethod
    def delete(cls, employee_id, *args, **kwargs):
        employee = cls.get_entity(employee_id)
        session.delete(employee)
        session.commit()


Employees = {
    POSTGRESQL_ENGINE: EmployeePostgres,
}

Employee = Employees[DB_ENGINE]
