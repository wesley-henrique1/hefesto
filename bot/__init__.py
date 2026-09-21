import sqlite3
import os

class ConectarDB:
    def __init__(self, caminho):
        self.DataBase = caminho
        pass
    def __conectar(self, sql: str, parametros: tuple = (), retornar_linha: bool= False):
        with sqlite3.connect(self.DataBase) as conn:
            cursor = conn.cursor()

            cursor.execute(self.__CriarTabela())
            cursor.execute(sql, parametros)
            if retornar_linha:
                Valr = cursor.fetchall()
                return Valr
            foi_alterado = cursor.rowcount > 0
            return foi_alterado

    def BuscarVlr(self):
        dicionario = {}

        query = f"""
        SELECT *
        FROM {self.NomeTabela}"""
        dados = self.__conectar(sql= query, retornar_linha= True)

        for linha in dados:
            dicionario[linha[0]] = {
                "VARIAVEL": linha[1],
                "PATH": linha[2],
                "ESTADO": linha[3],
            }
        return dicionario
    def DeletarVlr(self, valor: tuple):
        if os.path.exists(self.DataBase):
            os.remove(self.DataBase)
    def InserirVle(self, valor: tuple):
        query = f"INSERT INTO {self.NomeTabela} (CHAVES, TEXTO, ESTADO) VALUES (?, ?, ?)"  
        self.__conectar(sql= query, parametros= valor)   
        pass
