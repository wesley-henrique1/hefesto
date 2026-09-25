from src.lib import settings, admDB, modErros
from src.views import saidaGui
from tkinter import messagebox as msgbox
from pathlib import Path

import importlib
import time

validador = modErros.ModularErros(fonte= "MOD - EXECUTOR")
class executeMOD:
    def __init__(self,UI, listaMOD: list):
        self.ancoraUI = UI
        self.ancoraSaida = saidaGui

        ancoraPath = admDB.path_DB()
        self.dictPath = ancoraPath.BuscarVlr()

        _Caminho = settings._Caminho()
        self.localMOD = Path(_Caminho.PastaMod)

        self.importarMOD(listaMOD)
        pass

    def __AlimentarUI(self, fase: int, total: int, modulo: str, inicio: time.perf_counter):
        fim = time.perf_counter()
        tempo_segundos = fim - inicio
        texto = f"PROGRESSO: {fase}/{total} | {modulo}.py | tempo: {tempo_segundos:.0f}s"
        self.ancoraUI.contador.after(0, lambda t=texto: self.ancoraUI.contador.configure(text=t))

        pass    
    def __MontarCarregamento(self, log: list):
        listSafe = set()
        cabecalho = f"{'ARQUIVO':^46} | {'DATA':^12} | {'HORAS':^10}"
        divisor = "-" * len(cabecalho) + "\n"        
        tabela = cabecalho + "\n" + divisor

        for dictFase in log:
            arquivo = dictFase.get("ARQUIVO", "Sem Registro...")
            if len(arquivo) > 43:
                arquivo = arquivo[:43] + "..."
            if arquivo in listSafe:
                continue
            data = dictFase.get("DATA", "--/--/----")
            hora = dictFase.get("HORAS", "--:--:--")

            tabela += f"{arquivo:<46} | {data:^12} | {hora:^10}\n"
            listSafe.add(arquivo)

        widget_log = self.ancoraUI.logArquivo
        widget_log.configure(state="normal")
        widget_log.delete("0.0", "end")
        widget_log.insert("0.0", tabela)
        widget_log.configure(state="disabled")        
        pass
    def __TratarRota(self):
        for item in self.dictPath.values():
                caminho = item.get("PATH")
                item["PATH"] = Path(caminho)
        pass

    def importarMOD(self, listaMOD: list):
        self.listLog = []
        self.listSaida = []
        try:
            inicio = time.perf_counter()
            totalList = len(listaMOD)

            for dic in listaMOD:
                for nivel, chave in enumerate(dic.keys(), 1):
                    try:
                        nomeModulo = dic[chave]['_Modulo']
                        nomeClasse = dic[chave]['_classes']
                        self.__AlimentarUI(fase= nivel, total= totalList, modulo= nomeModulo, inicio= inicio)

                        caminho = self.localMOD / f"{nomeModulo}.py"
                        if not caminho.is_file():
                            msgbox.showerror("Erro de Módulo", f"O arquivo '{nomeModulo}.py' não existe na pasta de execução:\n{self.localMOD}")
                            return None

                        spec = importlib.util.spec_from_file_location(nomeModulo, str(caminho))
                    except Exception as e:
                        validador.registrar_log(e, "Constructor")
                    try:
                        if spec and spec.loader:
                            moduloCarregado = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(moduloCarregado)

                            if hasattr(moduloCarregado, nomeClasse):
                                classe_bot = getattr(moduloCarregado, nomeClasse)

                                self.__TratarRota()
                                instancia = classe_bot(self.dictPath)

                                booleano = instancia.pipeline()
                                if booleano:
                                    log = instancia.carregamento()
                                    saida = instancia.Saida()

                                if log or saida:
                                    self.listLog.extend(log)
                                    self.listSaida.extend(saida)
                            else:
                                msgbox.showerror(
                                    "Classe Não Encontrada",
                                    f"A classe estrutural '{nomeClasse}' não foi localizada dentro do arquivo '{caminho.name}'.\n\nVerifique se o nome da classe está correto no cadastro e no código-fonte."
                                )
                        else:
                            msgbox.showerror(
                                "Erro de Carregamento",
                                f"Não foi possível carregar as especificações (spec) do módulo para a classe '{nomeClasse}'.\n\nO arquivo pode estar corrompido, incompleto ou inacessível."
                            )
                    except Exception as e:
                        validador.registrar_log(e, f"Ponte -> {nomeModulo}")

            self.__MontarCarregamento(log= self.listLog)
            self.ancoraSaida.outputUI(self.listSaida)
        except Exception as e:
            validador.registrar_log(e, "Carregamento modulo")
            return None
