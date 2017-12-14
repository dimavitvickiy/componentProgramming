import psycopg2

from config import CONNECTION


class DataBaseUtil:
    def __init__(self, connection_config):
        self.connection = psycopg2.connect(connection_config)

    def modify(self, query):
        cursor = self.get_cursor()
        cursor.execute(query)
        returned_value = cursor.fetchone()
        self.save()
        if returned_value:
            return returned_value[0]

    def retrieve(self, query, many=True):
        cursor = self.get_cursor()
        cursor.execute(query)
        if many:
            result = [
                self.create_dict(values, cursor.description)
                for values in cursor.fetchall()
            ]
        else:
            entity = cursor.fetchone()
            result = self.create_dict(cursor.fetchone(), cursor.description) \
                if entity else None
        return result

    def get_cursor(self):
        return self.connection.cursor()

    @staticmethod
    def create_dict(values, column_names):
        return {
            column_name[0]: value
            for column_name, value in zip(column_names, values)
        }

    def save(self):
        self.connection.commit()


db = DataBaseUtil(CONNECTION)


if __name__ == '__main__':
    # HOST = '127.0.0.1'
    # DB_NAME = 'postgres'
    # USER = 'postgres'
    # PASSWORD = 'ma1der996'
    #
    # CONNECTION = "host='{}' dbname='{}' user='{}' password='{}'".format(
    #     HOST, DB_NAME, USER, PASSWORD)
    # db = DataBaseUtil(CONNECTION)
    employee_list = db.retrieve('''
        select first_name, last_name, name as subdivision from employees
        join subdivisions ON subdivision_id = subdivisions.id;
    ''')
    employee = db.retrieve(query='''select first_name, last_name, name as subdivision from employees
        join subdivisions ON subdivision_id = subdivisions.id where employees.id = {}'''.format(10), many=False)
    print(employee)
