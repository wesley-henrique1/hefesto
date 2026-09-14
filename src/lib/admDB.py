import sqlite3
from .caminhos import _DataBase

class ModuloDB:
    def __init__(self):
        self.moduloDB = _DataBase.modDb
        self.NomeTabela = "modulosTB"
        pass

        pass
    def __CriarTabela(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.NomeTabela} (
            CHAVES VARCHAR(8) PRIMARY KEY,
            NOME TEXT NOT NULL,
            MODULO TEXT NOT NULL,
            CLASSE TEXT NOT NULL,
            ESTADO VARCHAR(1) NOT NULL
        );
        """
        return query
    def __conectar(self, sql: str, parametros: tuple = (), retornar_linha: bool= False):
        with sqlite3.connect(self.moduloDB) as conn:
            cursor = conn.cursor()

            cursor.execute(self.__CriarTabela())
            cursor.execute(sql, parametros)
            if retornar_linha:
                return cursor.fetchall()

    def BuscarVlr(self):
        dicionario = {}

        query = f"""
        SELECT *
        FROM {self.NomeTabela}"""
        dados = self.__conectar(sql= query, retornar_linha= True)

        for linha in dados:
            dicionario[linha[0]] = {
                "_Nomenclatura": linha[1],
                "_Modulo": linha[2],
                "_classes": linha[3],
                "_estado": linha[4]
            }
        
        return dicionario
    def DeletarVlr(self, valor: tuple):
        query = f"DELETE FROM {self.NomeTabela} WHERE CHAVES = ?"
        self.__conectar(sql= query, parametros= valor)
        pass
    def EditarVlr(self, valor: tuple):
        query = f"""
            UPDATE {self.NomeTabela} 
            SET NOME = ?, MODULO= ?, CLASSE= ?, ESTADO = ?
            WHERE CHAVES =?
        """
        self.__conectar(sql= query, parametros= valor)
        pass
    def InserirVle(self, valor: tuple):
        query = f"INSERT INTO {self.NomeTabela} (CHAVES, NOME, MODULO, CLASSE, ESTADO) VALUES (?, ?, ?, ?, ?)"  
        self.__conectar(sql= query, parametros= valor)      
        pass