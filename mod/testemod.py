import datetime as dt
import pandas as pd


class auxiliares:
    def MontarRota(self, dictRota: dict):
        listBase = []       
        variaveis_validas = {"_8596", "_Saidas_"}
        for item in dictRota.values():
            if item.get("VARIAVEL") in variaveis_validas:
                listBase.append(item.get("PATH"))
        return listBase

    pass
class TesteMod(auxiliares):
    def __init__(self, rotas):
        self.rotas = self.MontarRota(dictRota= rotas)
        self.list_path = self.rotas[:-1]
        self.caminho = self.rotas[-1] / "Analitico Cadastro.xlsx"
        pass

    def pipeline(self):
        try:
            dataDados = pd.read_excel(str(self.list_path[0]), usecols= ['CODPROD', 'DESCRICAO', 'RUA', 'PREDIO'])
        except Exception as e:
            # self.validador.registrar_log(e, "Extract")
            print("Extract", e)
            return False
        try:
            filtro = dataDados.loc[dataDados['RUA'] == 1]
            filtro = filtro.loc[filtro['PREDIO'].between(1, 10)]
        except Exception as e:
            # self.validador.registrar_log(e, "Transform")
            print("Transform", e)

            return False
        try:
            filtro.to_excel(self.caminho, sheet_name= "Cadastro", index= False)
            return True
        except Exception as e:
            # self.validador.registrar_log(e, "Load")
            print("Load", e)
            return False
        
    def carregamento(self):
        lista_de_logs = []
        try:
            for path in self.list_path:
                nome_file = path.name
                data_file = path.stat().st_mtime
                data_modificacao = dt.datetime.fromtimestamp(data_file)
                data_formatada = data_modificacao.strftime("%d/%m/%Y")
                horas_formatada = data_modificacao.strftime("%H:%M:%S")
                dic_log = {
                    "ARQUIVO" : nome_file
                    ,"DATA" : data_formatada
                    ,"HORAS" : horas_formatada
                }
                lista_de_logs.append(dic_log)
            return lista_de_logs
        except Exception as e:
            # self.validador.registrar_log(e, "CARREGAMENTO")
            print("CARREGAMENTO", e)
            return False
    def Saida(self):
        return [self.caminho]
