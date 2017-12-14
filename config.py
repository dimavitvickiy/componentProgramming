HOST = '127.0.0.1'
PORT = 5432
DB_NAME = 'postgres'
USER = 'postgres'
PASSWORD = 'ma1der996'
POSTGRESQL_ENGINE = 'postgresql'
DB_ENGINE = POSTGRESQL_ENGINE


CONNECTION = f'{DB_ENGINE}+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'


UKRAINIAN_LANGUAGE = 'Ukrainian'
RUSSIAN_LANGUAGE = 'Russian'

LANGUAGE = RUSSIAN_LANGUAGE


def set_language(language):
    global LANGUAGE
    LANGUAGE = language


def get_language():
    return LANGUAGE
