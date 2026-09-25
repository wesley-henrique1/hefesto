from src.lib.settings import _DataBase, _DataJson
from typing import Literal

import os
import sqlite3

class ErroDB:
    def __init__(self):
        self.erroDB = _DataBase.errosdb
        self.NomeTabela = "errorTB"
        self.dic = {
            "PermissionError": "O arquivo está aberto por outro programa (como o Excel) ou você não tem permissão para acessá-lo. Feche o arquivo e tente novamente.",
            "FileNotFoundError": "O arquivo de origem não foi encontrado no caminho especificado. Verifique se ele está na pasta correta.",
            "EmptyDataError": "O arquivo encontrado está completamente vazio. Verifique a origem dos dados.",
            "BadZipFile": "O arquivo Excel parece estar corrompido ou não foi baixado completamente.",
            "KeyError": "Uma ou mais colunas obrigatórias não foram encontradas no arquivo de origem.",
            "TypeError": "Incompatibilidade no tipo de dado detectada durante o processamento.",
            "ValueError": "O formato de algum dado (como data ou número) está inválido ou fora do padrão esperado.",
            "IndexError": "Tentativa de acessar uma linha ou coluna que não existe na planilha ou base de dados.",
            "OperationalError": "Não foi possível conectar ao banco de dados. Verifique a rede ou se o servidor está ativo.",
            "ProgrammingError": "Erro interno na estrutura da query SQL ou a tabela/coluna informada não existe.",
            "IntegrityError": "Falha de integridade: tentativa de inserir um registro duplicado ou nulo onde não é permitido.",
            "FailSafeException": "A automação foi interrompida de emergência porque o ponteiro do mouse foi movido para o canto da tela.",
            "TclError": "Erro interno de renderização ou comportamento da interface gráfica.",
            "NameError": "Uma variável, componente ou função interna foi chamada mas não foi definida no sistema.",
            "ConnectionError": "Falha de conexão com a internet ou o servidor remoto recusou o acesso.",
            "Timeout": "O servidor demorou muito para responder. A operação foi cancelada para evitar travamentos do sistema.",
            "AttributeError": "O sistema tentou acessar uma propriedade ou função interna que não existe ou está indisponível.",
            "UnboundLocalError": "Não foi possível concluir a ação porque uma informação necessária não estava pronta a tempo. Tente novamente em instantes.",
            "Exception": "Ocorreu um erro inesperado no sistema. Entre em contato com o administrador."
        }
        pass

    def __CriarTabela(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.NomeTabela} (
            CHAVE TEXT PRIMARY KEY,
            DESC TEXT NOT NULL);
        """
        return query
    def _conectar(self):
        query_select = f"SELECT CHAVE FROM {self.NomeTabela}"
        query_insert = f"INSERT INTO {self.NomeTabela} (CHAVE, DESC) VALUES (?, ?)"
        query_final = f"SELECT * FROM {self.NomeTabela}"

        with sqlite3.connect(self.erroDB) as conn:
            cursor = conn.cursor()
            cursor.execute(self.__CriarTabela())

            cursor.execute(query_select)
            registros_existentes = cursor.fetchall()
            chaves_no_banco = {linha[0] for linha in registros_existentes}

            for chave, descricao in self.dic.items():
                if chave not in chaves_no_banco:
                    parametros = (
                            chave, 
                            descricao, 
                        )
                    cursor.execute(query_insert, parametros)
            cursor.execute(query_final)
            valor = cursor.fetchall()
            return valor
        pass

class KeysDB:
    def __init__(self):
        self.DataBase = _DataBase.keys
        self.NomeTabela = "keystb"
        pass
    def __CriarTabela(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.NomeTabela} (
            CHAVES TEXT NOT NULL,
            TEXTO TEXT NOT NULL,
            ESTADO TEXT NOT NULL
        );
        """
        return query
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
    def DeletarVlr(self):
        if os.path.exists(self.DataBase):
            os.remove(self.DataBase)
    def InserirVle(self, valor: tuple):
        query = f"INSERT INTO {self.NomeTabela} (CHAVES, TEXTO, ESTADO) VALUES (?, ?, ?)"  
        self.__conectar(sql= query, parametros= valor)   
        pass

class path_DB:
    def __init__(self):
        self.DataBase = _DataBase.rotadb
        self.NomeTabela = "rotaTB"
        self.botpath = _DataJson.rotas
        pass

    def __CriarTabela(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.NomeTabela} (
            CHAVES VARCHAR(8) PRIMARY KEY,
            VARIAVEL TEXT NOT NULL,
            PATH TEXT NOT NULL,
            ESTADO VARCHAR(1) NOT NULL
        );
        """
        return query

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
        query = f"DELETE FROM {self.NomeTabela} WHERE CHAVES = ?"
        sucesso = self.__conectar(sql= query, parametros= valor)
        return sucesso
    def EditarVlr(self, valor: tuple):
        query = f"""
            UPDATE {self.NomeTabela} 
            SET VARIAVEL = ?, PATH= ?, ESTADO= ?
            WHERE CHAVES =?
        """
        self.__conectar(sql= query, parametros= valor)
        pass
    def InserirVle(self, valor: tuple):
        query = f"INSERT INTO {self.NomeTabela} (CHAVES, VARIAVEL, PATH, ESTADO) VALUES (?, ?, ?, ?)"  
        self.__conectar(sql= query, parametros= valor)      
        pass
class Task_DB:
    def __init__(self):
        self.DataBase = _DataBase.taskDb
        self.NomeTabela = "taskTB"
        pass

    def __CriarTabela(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.NomeTabela} (
            CHAVES VARCHAR(8) PRIMARY KEY,
            NOME TEXT NOT NULL,
            DIAS TEXT NOT NULL,
            ESTADO VARCHAR(1) NOT NULL
        );
        """
        # TASK001 - Relatorio Corte - [2,3,4,5,6,7] - true
        return query
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
                "NOME": linha[1],
                "DIAS": linha[2],
                "ESTADO": linha[3],
            }
        return dicionario
    def DeletarVlr(self, valor: tuple):
        query = f"DELETE FROM {self.NomeTabela} WHERE CHAVES = ?"
        sucesso = self.__conectar(sql= query, parametros= valor)
        return sucesso
    def EditarVlr(self, valor: tuple):
        query = f"""
            UPDATE {self.NomeTabela} 
            SET NOME = ?, DIAS= ?, ESTADO= ?
            WHERE CHAVES =?
        """
        self.__conectar(sql= query, parametros= valor)
        pass
    def InserirVle(self, valor: tuple):
        query = f"INSERT INTO {self.NomeTabela} (CHAVES, NOME, DIAS, ESTADO) VALUES (?, ?, ?, ?)"  
        self.__conectar(sql= query, parametros= valor)      
        pass
class CRUD_DB:
    def __init__(self, base= Literal["modulos", "bots"]):
        match base:
            case "modulos":
                self.DataBase = _DataBase.modDb
                self.NomeTabela = "modulosTB"
            case "bots":
                self.DataBase = _DataBase.botdb
                self.NomeTabela = "botsTB"

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
        with sqlite3.connect(self.DataBase) as conn:
            cursor = conn.cursor()

            cursor.execute(self.__CriarTabela())
            cursor.execute(sql, parametros)
            if retornar_linha:
                return cursor.fetchall()
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
                "_Nomenclatura": linha[1],
                "_Modulo": linha[2],
                "_classes": linha[3],
                "_estado": linha[4]
            }
        
        return dicionario
    def DeletarVlr(self, valor: tuple):
        query = f"DELETE FROM {self.NomeTabela} WHERE CHAVES = ?"
        sucesso = self.__conectar(sql= query, parametros= valor)
        return sucesso
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