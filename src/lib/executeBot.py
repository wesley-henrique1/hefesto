import json
from .admDB import CRUD_DB, path_DB
from .settings import _Caminho, _DataJson
import pandas as pd
from pathlib import Path
import importlib.util
import os
class ExecuteBot:
    def __init__(self, chave: str, rotas: dict, entrada: Path, saida: Path,):
        self.dictJson = {
            'chave_modulo': chave,
            'textoUI': "INICIO",
            'fase': 0,
            'boleano': False
        }
        self.rotas = rotas
        self.entrada = str(entrada)
        self.saida = str(saida)

        ancora = CRUD_DB('bots')
        self.dicTemp = ancora.BuscarVlr()

        self.localBot = Path(_Caminho.PastaBot)
        self.local = self.localBot / 'status_bot.json'

        self.__CriarJson(local= self.local, dicionario= self.dictJson)
        self.__Importar(chave)
        pass

    def __CriarJson(self, local: Path, dicionario: dict):
        with open(local, mode= "w", encoding= "utf-8") as f:

            """
            validar depois uma forma de conversa escondida entre os modulos
            """
            json.dump(dicionario, f, ensure_ascii=False, indent=4)
            json.dumps(dicionario, ensure_ascii= False)
    
    def __SalvarApartir(self, valor):
        valor['boleano'] = False
        with open(self.local, "w", encoding="utf-8") as f:
            json.dump(valor, f, ensure_ascii=False, indent=4)

    def __Abrir(self):
        Status = json.loads(self.local.read_text(encoding="utf-8"))
        return Status
    
    def __ApagarJson(self):
        data = self.__Abrir()
        if not data['boleano'] and self.local.exists():
            os.remove(self.local)          
        
    def __Importar(self, chave):
        try:
            nomeClasse = self.dicTemp[chave]['_classes']
            print("\nTeste de passagem",nomeClasse)
            nomeModulo = self.dicTemp[chave]['_Modulo']

            arquivo_bot  = list(self.localBot.glob(nomeModulo + ".py"))
            if not arquivo_bot:
                print(f"Erro: O arquivo {nomeModulo}.py não foi encontrado na pasta {self.localBot}")
                return
            caminho = arquivo_bot[0]
        except Exception as e:
            print(f"\nerro na hr de procurar o arquivo .py {e}\n")
        try:
            spec = importlib.util.spec_from_file_location(nomeModulo, caminho)
            if spec and spec.loader:
                moduloCarregado = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(moduloCarregado)

                if hasattr(moduloCarregado, nomeClasse):
                    classe_bot = getattr(moduloCarregado, nomeClasse)

                    instancia = classe_bot(entrada= self.entrada, saida= self.saida, rotas= self.rotas)

                    valor = instancia._pipeline()
                    instancia._Simulador(valor)
                    print(valor)
                else:
                    print(f"Erro: A classe '{nomeClasse}' não foi encontrada no arquivo {arquivo_bot.name}")
            else:
                print(f"Erro ao carregar o spec do módulo: {nomeClasse}")
        except Exception as e:
            print(f"\nerro na etapa de modularização: {e}\n")