from models.abstract import DBAbstraction
from services.db import db


class Employee:
    def __init__(self, id_, first_name, last_name, subdivision):
        self.id = id_
        self.first_name = first_name
        self.last_name = last_name
        self.subdivision = subdivision


class EmployeeDB(DBAbstraction):
    GET_LIST_QUERY = '''
        SELECT employees.id, first_name, last_name, subdivisions.name AS subdivision
        FROM employees JOIN subdivisions ON subdivisions.id = employees.subdivision_id
        {where_cause}
        ORDER BY employees.id;
    '''
    GET_ENTITY_QUERY = '''
        SELECT employees.id, first_name, last_name, name as subdivision
        FROM employees JOIN subdivisions ON employees.subdivision_id = subdivisions.id
        WHERE employees.id = '{}';
    '''
    CREATE_QUERY = '''
        INSERT INTO employees (first_name, last_name, subdivision_id)
        VALUES ('{}', '{}', (select id from subdivisions where name='{}'))
        RETURNING employees.id;
    '''
    UPDATE_QUERY = '''
        UPDATE employees 
        SET first_name = '{}', last_name = '{}', subdivision_id = (select id from subdivisions where name='{}')
        WHERE id = '{}'
    '''
    DELETE_QUERY = '''
        DELETE FROM employees 
        WHERE id = '{}'
    '''

    @classmethod
    def get_list(cls, **kwargs):
        where_cause = build_where(kwargs)
        employee_list = db.retrieve(cls.GET_LIST_QUERY.format(where_cause=where_cause), many=True)
        return [
            Employee(
                employee['id'],
                employee['first_name'],
                employee['last_name'],
                employee['subdivision'],x`
            ) for employee in employee_list
        ]

    @classmethod
    def get(cls, employee_id):
        employee = db.retrieve(cls.GET_ENTITY_QUERY.format(employee_id), many=False)
        return Employee(
            employee['id'],
            employee['first_name'],
            employee['last_name'],
            employee['subdivision'],
        )

    @classmethod
    def create(cls, employee):
        new_employee_id = db.modify(
            cls.CREATE_QUERY.format(
                employee.first_name,
                employee.last_name,
                employee.subdivision,
            )
        )
        return new_employee_id

    @classmethod
    def delete(cls, employee_id):
        db.modify(cls.DELETE_QUERY.format(employee_id))

    @classmethod
    def update(cls, employee, first_name=None, last_name=None, subdivision=None):
        first_name = first_name or employee.first_name
        last_name = last_name or employee.last_name
        subdivision = subdivision or employee.subdivision
        db.modify(
            cls.UPDATE_QUERY.format(
                first_name,
                last_name,
                subdivision,
                employee.id
            )
        )


def build_where(where):
    if where:
        WHERE = 'where '
        where_string = WHERE
        for key, value in where.items():
            if where_string != WHERE:
                where_string += "and "
            where_string += "{key}='{value}'".format(key=key, value=value)
        return where_string
    return ''


if __name__ == '__main__':
    employee = Employee(None, 'a', 'b', 'Отдел Разработки')
    returned_value = EmployeeDB.create(employee)
    print(returned_value)
