import pandas as pd
from pathlib import Path

import time
import pyperclip as pc
import pyautogui as pag
    

class auxiliar:
    def _conversaUI(self, fase, total_itens, tempo):
        """
        Atualiza a interface gráfica do bot em tempo real com o progresso atual,
        calculando o tempo decorrido e exibindo os itens restantes.
        """
        if hasattr(self, 'cancel_event') and self.cancel_event.is_set():
            return
            
        fim = time.perf_counter()
        tempo_segundos = fim - tempo
        texto = f"Progresso: {fase}/{total_itens} | faltando: {total_itens - fase} | {tempo_segundos:.0f}s"

        # Verifica de forma segura se o componente de UI e o contador existem antes de atualizar
        if hasattr(self, 'ancoraUI') and self.ancoraUI:
            if hasattr(self.ancoraUI, 'contador') and self.ancoraUI.contador:
                try:
                    self.ancoraUI.contador.after(0, lambda t=texto: self.ancoraUI.contador.configure(text=t))
                except Exception:
                    pass

    def _sleep_verificando(self, segundos, cancel_event, _parar_execucao):
        """
        Realiza uma pausa (sleep) fracionada e inteligente, verificando periodicamente
        se o usuário solicitou a parada ou o cancelamento da execução.
        """
        passos = int(segundos * 10)
        for _ in range(max(1, passos)):
            if _parar_execucao or (cancel_event and cancel_event.is_set()):
                return False
            time.sleep(segundos / max(1, passos))
        return True
    
    def _copiar_e_validar(valor, tentativas=5):
        """
        Copia um valor para a área de transferência do sistema operacional e valida
        repetidamente se foi copiado com sucesso antes de permitir a continuação.
        """
        str_valor = str(valor)
        pc.copy(str_valor)
        for _ in range(tentativas):
            if pc.paste() == str_valor:
                return True
            pag.sleep(0.1)
            pc.copy(str_valor)
        return False
    
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
        # 1. Extração de dados
        try:
            # Lógica de extração aqui
            pass
        except Exception as e:
            print("Erro na Extração:", e)
            return False

        # 2. Tratamento / Transformação de dados
        try:
            # Lógica de tratamento aqui
            pass
        except Exception as e:
            print("Erro na Tratamento:", e)
            return False

        # 3. Carga / Salvamento dos dados
        try:
            # Lógica de carga aqui
            # Sempre retorna um valor numérico (int ou float) indicando o total processado/carregado
            return 1
        except Exception as e:
            print("Erro na Carga:", e)
            return False
            
    def _simulador(self, df: pd.DataFrame, cancel_event=None):
        try:
            lista = []
            total_itens = len(df)
            inicio = time.perf_counter()
            
            for fase, (_, registro) in enumerate(df.iterrows(), 1):
                if self._parar_execucao or (cancel_event and cancel_event.is_set()): break
                
                auxiliar._conversaUI(self, fase=fase, total_itens=total_itens, tempo= inicio)

                # Pode colocar esse formato pelo decorrer do codigo, vai parar o script ou pausar para da respito
                if not auxiliar._sleep_verificando(self.velocidade, self._parar_execucao, cancel_event): break

                """A QUI PODE DA SEQUENCIA NAS INSTRUÇÁO DO pyperclip OU pyautogui"""

                """Aqui vai esta alimentando a lista com as fase para depois validar se mandou tudo correto"""
                lista.append(fase)
            return len(lista)
        except Exception as e:
            print("simulador", e)