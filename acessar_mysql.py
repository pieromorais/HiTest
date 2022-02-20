import sqlalchemy as db
from decouple import config as c

config = {
    'host': 'localhost',
    'port': 3306,
    'user': c('DB_USER'),
    'password': c('DB_PASS'),
    'database': 'hi_database'
}

db_user = config.get('user')
db_pwd = config.get('password')
db_host = config.get('host')
db_port = config.get('port')
db_name = config.get('database')

# connection str
connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'

# connect to database
engine = db.create_engine(connection_str)
connection = engine.connect()

print(connection)   