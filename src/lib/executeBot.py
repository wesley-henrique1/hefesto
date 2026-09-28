from src.lib.settings import _Caminho, _DataBase
from src.lib.admDB import CRUD_DB, KeysDB
from src.lib.modErros import ModularErros
from tkinter import messagebox as msgbox
from pathlib import Path
import importlib.util

import os
validador = ModularErros(fonte= "BOT - EXECUTOR")
class ExecuteBot:
    def __init__(self, UI, chave: str, rotas: dict, entrada: Path, saida: Path):
        self.ancoraUI = UI
        self.rotas = rotas
        self.entrada = str(entrada)
        self.saida = str(saida)
        ancora = CRUD_DB('bots')
        self.dicTemp = ancora.BuscarVlr()

        self.localBot = Path(_Caminho.PastaBot)

        self.instancia_atual = None
        self.valor_atual = None
        self.chave = chave

    def Controladora(self, boleano: bool):
        self.instancia_atual.Controladora(boleano)
        pass

    def carregar_modulo(self):
        try:
            nomeClasse = self.dicTemp[self.chave]['_classes']
            nomeModulo = self.dicTemp[self.chave]['_Modulo']
            if not nomeModulo or nomeModulo.strip().lower() in [".venv", "venv", "env"]:
                validador.registrar_log(f"Tentativa inválida de execução do módulo restrito: {nomeModulo}", "Segurança Módulo")
                msgbox.showwarning("Acesso Negado", "O módulo selecionado é restrito e não pode ser executado.")
                return None
            arquivo_bot = list(self.localBot.glob(nomeModulo + ".py"))
            if not arquivo_bot:
                msgbox.showerror("Erro de Módulo", f"O arquivo '{nomeModulo}.py' não existe na pasta de execução:\n{self.localBot}")
                return None
            caminho = arquivo_bot[0]
        except Exception as e:
            validador.registrar_log(e, "Carregamento modulo")
            return None

        try:
            spec = importlib.util.spec_from_file_location(nomeModulo, caminho)

            if spec and spec.loader:
                moduloCarregado = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(moduloCarregado)
                
                if hasattr(moduloCarregado, nomeClasse):
                    classe_bot = getattr(moduloCarregado, nomeClasse)

                    self.instancia_atual = classe_bot(
                        UI= self.ancoraUI,
                        entrada=self.entrada, 
                        saida=self.saida, 
                        rotas=self.rotas, 
                    )
                    try:
                        self.valor_atual = self.instancia_atual._pipeline()
                        self.ancoraUI.contagem.configure(text= f"Total de Valores a serem processados: {self.valor_atual['CODPROD'].nunique()}")
                        return self.valor_atual
                    except Exception as e:
                        validador.registrar_log(e, "execute_pipeline")
                        return None
                else:
                    msgbox.showerror(
                        "Classe Não Encontrada",
                        f"A classe estrutural '{nomeClasse}' não foi localizada dentro do arquivo '{arquivo_bot.name}'.\n\nVerifique se o nome da classe está correto no cadastro e no código-fonte."
                    )
            else:
                msgbox.showerror(
                    "Erro de Carregamento",
                    f"Não foi possível carregar as especificações (spec) do módulo para a classe '{nomeClasse}'.\n\nO arquivo pode estar corrompido, incompleto ou inacessível."
                )
        except Exception as e:
            validador.registrar_log(e, "execute_Modulo")
        
        return None

    def executar_simulador(self, cancel_event=None):
        try:
            if not self.instancia_atual or self.valor_atual is None:
                msgbox.showwarning("Nenhuma Execução", "Não há nenhuma execução pendente...")
                return

            self.instancia_atual._Simulador(self.valor_atual, cancel_event=cancel_event)
        except Exception as e:
            validador.registrar_log(e, "Simulador")