import json
from admDB import CRUD_DB
from settings import _Caminho
from pathlib import Path
import importlib.util
import os
class ExecuteBot:
    def __init__(self, chave):
        self.ancora = CRUD_DB('bots')
        self.dicTemp = self.ancora.BuscarVlr()
        self.localBot = Path(_Caminho.PastaBot)
        self.dictJson = {
            'chave_modulo': chave,
            'textoUI': "INICIO",
            'fase': 0,
            'boleano': False
        }
        self.local = self.localBot / 'status_bot.json'
        self.__CriarJson()
        self.__Importar(chave)
        self.__ApagarJson()
        pass

    def __CriarJson(self):
        with open(self.local, "w", encoding= "utf-8") as f:
            json.dump(self.dictJson, f, ensure_ascii=False, indent=4)
    
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
        nomeClasse = self.dicTemp[chave]['_classes']
        nomeModulo = self.dicTemp[chave]['_Modulo']

        arquivo_bot  = list(self.localBot.glob(nomeModulo + ".py"))
        if not arquivo_bot:
            print(f"Erro: O arquivo {nomeModulo}.py não foi encontrado na pasta {self.localBot}")
            return
        caminho = arquivo_bot[0]

        spec = importlib.util.spec_from_file_location(nomeModulo, caminho)
        if spec and spec.loader:
            moduloCarregado = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(moduloCarregado)

            if hasattr(moduloCarregado, nomeClasse):
                classe_bot = getattr(moduloCarregado, nomeClasse)
                while True:
                    instancia = classe_bot()
                    valor = self.__Abrir()
                    print("Interface:",valor['textoUI'])
                    if not valor['boleano']:
                        break
                    else:
                        self.__SalvarApartir(valor)
            else:
                print(f"Erro: A classe '{nomeClasse}' não foi encontrada no arquivo {arquivo_bot.name}")
        else:
            print(f"Erro ao carregar o spec do módulo: {nomeClasse}")

if __name__ == "__main__":
    ExecuteBot('MOD_001')