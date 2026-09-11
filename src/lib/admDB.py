import sqlite3
from .caminhos import _DataBase

class ADM_dB:
    def __init__(self):
        pass


    def CriarMOD(self):
        caminho = _DataBase.modDb
        caminho.parent.mkdir(parents= True, exist_ok= True)

        with sqlite3.connect(caminho) as conexao:
            cursor  = conexao.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS modDB (
                    ID              TEXT PRIMARY KEY,
                    NOMECLATURA     TEXT,
                    MODULO          TEXT,
                    CLASSE          TEXT,
                    ESTADO          BOOL,
                )
            """)
            conexao.commit()
            print(f"Banco e tabela criados com sucesso em: {caminho}")