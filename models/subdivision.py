from models.abstract import DBAbstraction
from services.db import db


class Subdivision:
    def __init__(self, id_, name):
        self.id = id_
        self.name = name


class SubdivisionDB(DBAbstraction):
    GET_LIST_QUERY = '''
        SELECT id, name
        FROM subdivisions
    '''
    GET_ENTITY_QUERY = '''
        SELECT id, name
        FROM subdivisions
        WHERE id = {};
    '''
    CREATE_QUERY = '''
        INSERT INTO subdivisions (name)
        VALUES ({})
        RETURNING id;
    '''
    UPDATE_QUERY = '''
        UPDATE subdivisions 
        SET name = {}
        WHERE id = {}
    '''
    DELETE_QUERY = '''
        DELETE FROM subdivisions
        WHERE id = {}
    '''

    @classmethod
    def get_list(cls):
        subdivision_list = db.retrieve(cls.GET_LIST_QUERY, many=True)
        return [
            Subdivision(
                subdivision['id'],
                subdivision['name'],
            ) for subdivision in subdivision_list
        ]

    @classmethod
    def get(cls, subdivision_id):
        subdivision = db.retrieve(cls.GET_ENTITY_QUERY.format(subdivision_id), many=False)
        return Subdivision(
            subdivision['id'],
            subdivision['name'],
        )

    @classmethod
    def create(cls, subdivision):
        db.modify(
            cls.CREATE_QUERY.format(
                subdivision.name,
            )
        )

    @classmethod
    def delete(cls, subdivision_id):
        db.modify(cls.DELETE_QUERY.format(subdivision_id))

    @classmethod
    def update(cls, subdivision, name=None):
        name = name or subdivision.name
        db.modify(
            cls.UPDATE_QUERY.format(
                name,
                subdivision.id
            )
        )
