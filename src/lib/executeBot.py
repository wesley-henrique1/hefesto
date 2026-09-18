import json
from .admDB import CRUD_DB, path_DB
from .settings import _Caminho, _DataJson
import pandas as pd
from pathlib import Path
import importlib.util
import os
class ExecuteBot:
    def __init__(self, chave, entrada, saida, rotas):
        self.ancora = CRUD_DB('bots')
        self.entrada = entrada
        self.rotas = rotas
        self.saida = saida

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

                instancia = classe_bot(entrada= str(self.entrada), saida= self.saida, rotas= self.rotas)

                valor = instancia._pipeline()
                print(valor)
            else:
                print(f"Erro: A classe '{nomeClasse}' não foi encontrada no arquivo {arquivo_bot.name}")
        else:
            print(f"Erro ao carregar o spec do módulo: {nomeClasse}")

if __name__ == "__main__":
    rota = path_DB()
    dictRotas = rota.BuscarVlr()
    for chave, dados in dictRotas.items():
        if dados.get('VARIAVEL') == "_OutPut_":
            caminho = Path(dados.get('PATH', ''))
            break
    if not caminho:
        print("Erro: Caminho de output não foi configurado.")

    caminho.mkdir(parents=True, exist_ok=True)
    
    Entrada = caminho / "EntradaBot.xlsx"
    Saida = caminho / "SaidaBot.xlsx"
    if not os.path.exists(Entrada):
        etapas = {
            'transferencia': ["CODPROD"],
            "Retirada": ['CODPROD', 'DTULTENT', 'QTESTGER', 'OBSFL'],
            'transf3707': ["CODPROD", "DESTINO"],
            'Etapa_3': ["CODPROD", "PL_LASTRO", "PL", "CAP", "QTEnd", "V_CAP"],
            'adiconarPK': ["CODPROD", "DESTINO", 'CAPACIDADE', 'PONTO_REP']
        }

        with pd.ExcelWriter(Entrada, engine='openpyxl') as writer:
            for nome_aba, colunas in etapas.items():
                pd.DataFrame(columns=colunas).to_excel(writer, sheet_name=nome_aba, index=False)


    ExecuteBot(chave='BOT_001', entrada= Entrada,saida= Saida, rotas= dictRotas)