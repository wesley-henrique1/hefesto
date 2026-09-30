from bot import ConectarDB
import pandas as pd
from pathlib import Path
import time
import pyperclip as pc
import pyautogui as pag
import os
    
class auxiliar:
    def conversaUI(self, fase, total_itens, tempo_segundos):
        if hasattr(self, 'cancel_event') and self.cancel_event.is_set():
            return

        texto = f"Progresso: {fase}/{total_itens} | faltando: {total_itens - fase} | {tempo_segundos:.0f}s"

        if hasattr(self, 'ancoraUI') and self.ancoraUI:
            if hasattr(self.ancoraUI, 'contador') and self.ancoraUI.contador:
                try:
                    self.ancoraUI.contador.after(0, lambda t=texto: self.ancoraUI.contador.configure(text=t))
                except Exception:
                    pass
    def _copiar_e_validar(valor, tentativas=5):
        str_valor = str(valor)
        pc.copy(str_valor)
        for _ in range(tentativas):
            if pc.paste() == str_valor:
                return True
            pag.sleep(0.1)
            pc.copy(str_valor)
        return False

class TesteBot:
    def __init__(self,UI, rotas: dict, entrada: Path, saida: Path):
        self.ancoraUI = UI
        self._parar_execucao = False
        self.velocidade = 0.05
        self.rota = rotas

        self.saida = saida
        self.Entrada = str(entrada)
        pass
    def Controladora(self, valor: bool = True):
        self._parar_execucao = valor
    def _pipeline(self):
        try:
            pass
        except Exception as e:
            print("extrair", e)
        try:
            pass
        except Exception as e:
            print("Tratamento", e)
        try:
            pass
        except Exception as e:
            print("Carga", e)
    def _Simulador(self, df: pd.DataFrame, cancel_event=None):
        try:
            lista = []
            total_itens = len(df)
            inicio = time.perf_counter()
            
            def sleep_verificando(segundos):
                passos = int(segundos * 10)
                for _ in range(max(1, passos)):
                    if self._parar_execucao or (cancel_event and cancel_event.is_set()):
                        return False
                    time.sleep(segundos / max(1, passos))
                return True

            for fase, (_, registro) in enumerate(df.iterrows(), 1):
                if self._parar_execucao or (cancel_event and cancel_event.is_set()): break

                fim = time.perf_counter()
                auxiliar.conversaUI(self, fase=fase, total_itens=total_itens, tempo_segundos=fim - inicio)
                
                if not sleep_verificando(self.velocidade): break

                # --- ETAPA 1: Inserir Código do Produto ---
                cod_prod = registro['CODPROD']
                if not auxiliar._copiar_e_validar(cod_prod):
                    continue
                pag.hotkey("ctrl", "v")
                                    
                if not sleep_verificando(self.velocidade): break
                    
                pag.press('enter')

                # --- ETAPA 2: Inserir Endereço ---
                destino = registro['DESTINO']
                if not auxiliar._copiar_e_validar(destino):
                    continue
                pag.hotkey("ctrl", "v")
                
                if not sleep_verificando(self.velocidade): break
                for _ in range(3):
                    if self._parar_execucao or (cancel_event and cancel_event.is_set()):
                        break
                    pag.press('enter')
                lista.append(fase)
            return len(lista)
        except Exception as e:
            print("simulador", e)