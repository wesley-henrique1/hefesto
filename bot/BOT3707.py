from pathlib import Path
import sys
RAIZ = Path(__file__).resolve().parent.parent
sys.path.append(str(RAIZ))

import pyautogui as pag
import pyperclip as pc

from datetime import datetime,timedelta
from pathlib import Path

import pandas as pd
import numpy as np
import json
import time
import os

class auxiliar:
    def PuxarRotas(rotas: dict):
        listaRota = []
        for chave, dados in rotas.items():
            etapa = dados.get('VARIAVEL')
            match etapa:
                case "_endereco07":
                    caminho = Path(dados.get('PATH', ''))
                    listaRota.append(str(caminho))
        return listaRota
    # def Casamento(rota):
    #     caminho = Path(r'C:\MESTRE_COD\projetos\hefesto\bot\status_bot.json')
    #     dictStatus = json.loads(caminho.read_text(encoding="utf-8"))
        pass
    def limpar_terminal() -> None:
        os.system("cls" if os.name == "nt" else "clear")

        pass
    def ajuste_numeros(df: pd.DataFrame, colunas: list[str]):
        """Converte colunas de texto formatadas em moeda/número pt-BR para float de forma performática."""
        for col in colunas:
            if col in df.columns:
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.replace(".", "", regex=False)
                    .str.replace(",", ".", regex=False)
                )
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(-1).astype(float)
        return df
    def _copiar_e_validar(valor, tentativas=5):
        """Garante que o valor foi devidamente copiado para a área de transferência."""
        str_valor = str(valor)
        pc.copy(str_valor)
        for _ in range(tentativas):
            if pc.paste() == str_valor:
                return True
            pag.sleep(0.1)
            pc.copy(str_valor)
        return False
    def exibir_info_arquivos(paths: list[str]) -> None:
        """Exibe o cabeçalho padronizado com nome e data de modificação dos arquivos."""
        print("=" * 60)
        for caminho in paths:
            if os.path.exists(caminho):
                nome = os.path.basename(caminho)
                timestamp = os.path.getmtime(caminho)
                data_formatada = datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M:%S")
                print(f"[ARQUIVO]: {nome}\n"
                      f"[MODIFICADO EM]: {data_formatada}\n")
            else:
                print(f"[ALERTA]: Arquivo não encontrado -> {caminho}")
        print("=" * 60 + "\n")

    
class TransferirPROD:
    def __init__(self, entrada, saida, rotas):
        self.largura = 71
        self.valvula_salva = False
        self.velocidade = 0.24

        var = auxiliar.PuxarRotas(rotas)
        self.listaPath = [entrada] + var
        self.listaSave = [saida]
        self.totalItens = 0
        self.processados = 0 
        self.statusTexto = "Aguardando..."
        self.ativo = True
        print(self.listaPath)

    def _pipeline(self):
        lista_de_tarefas = [1, 2, 3, 4, 5]
        self.total_itens = len(lista_de_tarefas)
        self.processados = 0
        
        for item in lista_de_tarefas:
            if not self.ativo:
                break
            time.sleep(1) 
            self.processados += 1
            self.status_texto = f"Processando item {item}"
        return self.processados
       
    # def _pipeline(self):
    #     try:
    #         Endereco = [
    #             'COD_END'
    #             ,'PREDIO'
    #             ,'NIVEL'
    #             ,'APTO'
    #             ,'STATUS'
    #             ,'COD'
    #             ,'DESC'
    #             ,'DT_ENTRADA'
    #             ,'DT_VALIDADE'
    #             ,'EMB'
    #             ,'LASTRO'
    #             ,'CAMADA'
    #             ,'CAP'
    #             ,'TIPO_PK'
    #             ,'PL_END'
    #             ,'QTDE'
    #             ,'ENTRADA'
    #             ,'SAIDA'
    #             ,'DISP'
    #         ]

    #         base_dados = pd.read_excel(self.listaPath[0], sheet_name= 'transf3707')
    #         endereco = pd.read_csv(self.listaPath[1], header=None, names= Endereco, dtype=str)
    #     except Exception as e:
    #         print('Extract', e)
    #         # self.validador.registrar_log(e, "Extract")
    #         return False  
    #     try:
    #         end = endereco.query("TIPO_PK == 'AP'")[["COD_END", "COD", "TIPO_PK", "ENTRADA", "SAIDA", "DISP"]].copy()
    #         end = auxiliar.ajuste_numeros(end, ["ENTRADA", "SAIDA", "DISP"])
    #         end["MOVI"] = end["ENTRADA"] + end["SAIDA"]

    #         livre = (end["DISP"] == 0) & (end["MOVI"] == 0)
    #         pendencias = end["MOVI"] > 0
    #         ocupado = end["DISP"] > 0
    #         negativado = end["DISP"] < 0

    #         end["CATEG_PROD"] = np.select(
    #             [livre, pendencias, ocupado, negativado],
    #             ["Livre", "Pendente", "Ocupado", "Negativado"],
    #             default="Validar",
    #         )
    #         end["CODPROD"] = pd.to_numeric(end["COD"], errors="coerce").fillna(0).astype(int)
            
    #         corte = end[['COD_END']]
    #         corte["CATEG_PK"] = pd.to_numeric(corte["COD_END"], errors="coerce").fillna(0).astype(int)
    #         corte = corte.drop(columns= 'COD_END')

    #         base_dados["CODPROD"] = pd.to_numeric(base_dados["CODPROD"], errors="coerce").fillna(0).astype(int)
    #         base_dados["DESTINO"] = pd.to_numeric(base_dados["DESTINO"], errors="coerce").fillna(0).astype(int)

    #         Produtos = base_dados.merge(end, on= 'CODPROD', how= 'left').drop(columns= 'COD')
    #         Produtos = Produtos.merge(corte, left_on= "DESTINO", right_on= "CATEG_PK", how= "left")

    #         Produtos['CATEG_PK'] = np.where(Produtos['CATEG_PK'].notna(), "Ocupado", "Livre")

    #         dfProntos = Produtos.loc[Produtos['CATEG_PK'] == 'Livre']
    #         dfPendentes = Produtos.loc[~Produtos['CATEG_PK'] == 'Livre']
    #         print(end)
    #     except Exception as e:
    #         print('Transform', e)
    #         # self.validador.registrar_log(e, "Transform")
    #         return False
    #     try:
    #         dfProntos = dfProntos.drop_duplicates(subset= 'CODPROD', keep= "last")
    #         with pd.ExcelWriter(self.listaSave[0], engine= 'openpyxl') as var:
    #             dfProntos.to_excel(var, sheet_name= "Transferidos", index= False)
    #             dfPendentes.to_excel(var, sheet_name= "Pendencias", index= False)
    #             self.valvula_salva = True
    #             print("etapa Load")
    #         return dfProntos
    #     except Exception as e:
    #         print('Load', e)
    #         self.validador.registrar_log(e, "Load")
    #         return False      
    # def _Simulador(self, df: pd.DataFrame):
    #     try:
    #         lista = []
    #         total_itens = len(df)
    #         inicio = time.perf_counter()
    #         for fase, (_, registro) in enumerate(df.iterrows(), 1):
    #             pag.sleep( self.velocidade)

    #             # --- ETAPA 1: Inserir Código do Produto ---
    #             cod_prod = registro['CODPROD']
    #             if not auxiliar._copiar_e_validar(cod_prod):
    #                 print(f"\nErro ao copiar produto: {cod_prod}")
    #                 continue
    #             pag.sleep( self.velocidade)
    #             pag.hotkey("ctrl", "v")
    #             pag.sleep( self.velocidade)
    #             pag.press('enter')

    #             # --- ETAPA 2: Inserir Endereço ---
    #             destino = registro['DESTINO']
    #             if not auxiliar._copiar_e_validar(destino):
    #                 print(f"Erro ao copiar endereço: {destino}")
    #                 continue
    #             pag.sleep( self.velocidade)
    #             pag.hotkey("ctrl", "v")
    #             pag.sleep( self.velocidade)

    #             for _ in range(3):
    #                 pag.press('enter')

    #             # Sucesso do item atual
    #             fim = time.perf_counter()
    #             tempo_segundos = fim - inicio
    #             lista.append(fase)

    #         return len(lista)
    #     except Exception as e:
    #         print('simulador')
    #         # ValidarErros(e, etapa="simulador")

if __name__ == "__main__":
    TransferirPROD()