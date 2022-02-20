import sqlalchemy as db
from decouple import config as c
from sqlalchemy.orm import sessionmaker

class ConnBase():

    def __init__(self) -> None:
        # dados para conectar no DB
        self.config = {
            'host': 'localhost',
            'port': 3306,
            'user': c('DB_USER'),
            'password': c('DB_PASS'),
            'database': 'hi_database',
            'charset': 'utf8mb4'
        }

        self.db_user = self.config.get('user')
        self.db_pwd = self.config.get('password')
        self.db_host = self.config.get('host')
        self.db_port = self.config.get('port')
        self.db_name = self.config.get('database')

        # connection str
        self.connection_str = f'mysql+pymysql://{self.db_user}:{self.db_pwd}@{self.db_host}:{self.db_port}/{self.db_name}'

        # connect to database
        engine = db.create_engine(self.connection_str)
        self.Session = sessionmaker(bind=engine)

        # criando conexão
        self.connection = engine.connect()

    def insert_to_table(self, userid, tweet_text, regra):

        # comando em sql para inserir dados na tabela
        str_model = "INSERT INTO tweets_table (user_id, tweet_text, regra) VALUES (%s, %s, %s);"
        # tupla com dados
        dados = (userid, tweet_text, regra)    

        # executa o comando insert
        self.connection.execute(str_model, dados)
        
        session = self.Session()
        # salva no banco de dados
        session.commit()