from src.lib import settings, admDB, modErros
from src.views import saidaGui
from tkinter import messagebox as msgbox
from pathlib import Path
import datetime as dt
import importlib.util
import time
import sys
validador = modErros.ModularErros(fonte="MOD - EXECUTOR")


class executeMOD:
    def __init__(self, UI, listaMOD: list):
        self.ancoraUI = UI
        self.ancoraSaida = saidaGui

        ancoraPath = admDB.path_DB()
        self.dictPath = ancoraPath.BuscarVlr()

        self.localMOD: Path = settings._Caminho.PastaMod  
        self.pasta_log: Path = settings._Caminho.PastaLog  
        self.pasta_log.mkdir(parents=True, exist_ok=True)

        self.listCarregar = []
        self.listSaida = []
        self.listLog = []

        self.importarMOD(listaMOD)

    @property
    def __dtHoje(self) -> dt.date:
        return dt.date.today()

    @property
    def __hora_atual(self) -> str:
        return dt.datetime.now().strftime("%H:%M:%S")

    def __AlimentarUI(self, fase: int, total: int, modulo: str, inicio: float):
        fim = time.perf_counter()
        tempo_segundos = fim - inicio
        texto = f"PROGRESSO: {fase}/{total} | {modulo}.py | tempo: {tempo_segundos:.0f}s"
        self.ancoraUI.contador.after(0, lambda t=texto: self.ancoraUI.contador.configure(text=t))

    def __ApagarLogsAntigos(self):
        anterior = self.__dtHoje - dt.timedelta(days=15)

        for item in self.pasta_log.iterdir():
            if not item.is_file():
                continue

            try:
                if item.suffix.lower() != ".txt":
                    item.unlink()
                    continue

                data_arquivo = dt.datetime.fromtimestamp(item.stat().st_mtime).date()
                if data_arquivo < anterior:
                    item.unlink()

            except Exception as e:
                validador.registrar_log(e, f"Limpeza logs {item.name}")

    def __GravarEmArquivo(self, bloco_texto: str):
        data_str = self.__dtHoje.strftime("%Y-%m-%d")
        nametag = f"Executados_{data_str}.txt"
        local = self.pasta_log / nametag

        ja_existe = local.exists()

        with open(local, mode="a", encoding="utf-8") as f:
            if not ja_existe:
                f.write("=== LOG INICIADO ===\n\n")
            f.write(bloco_texto + "\n")

    def __RegistrarLogTabela(self, listaLogs: list):
        if not listaLogs:
            return
        self.__ApagarLogsAntigos()

        linha = "=" * 56 + "\n"
        conteudo = f"Executado: {self.__hora_atual}\n"
        head = f"{'Nome':<14} | {'Pipeline':^10} | {'Carregamento':^12} | {'Retornos':^10}\n"
        divisor = "-" * len(head.strip()) + "\n"

        linhas_registros = ""
        for item in listaLogs:
            nome = str(item.get("nome", "Desconhecido"))
            pipeline = str(item.get("pipeline", "not"))
            carregamento = str(item.get("carregamento", "not"))
            retorno = str(item.get("retorno", "not"))

            linhas_registros += f"{nome:<14} | {pipeline:^10} | {carregamento:^12} | {retorno:^10}\n"

        completo = f"{linha}{conteudo}{head}{divisor}{linhas_registros}{linha}"
        self.__GravarEmArquivo(completo)
    def __MontarCarregamento(self, log: list):
        listSafe = set()
        cabecalho = f"{'ARQUIVO':^46} | {'DATA':^12} | {'HORAS':^10}"
        divisor = "-" * len(cabecalho)
        tabela = f"{cabecalho}\n{divisor}\n"

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
        def atualizar_texto():
            widget_log.configure(state="normal")
            widget_log.delete("0.0", "end")
            widget_log.insert("0.0", tabela)
            widget_log.configure(state="disabled")

        self.ancoraUI.contador.after(0, atualizar_texto)    
    def __TratarRota(self):
        for item in self.dictPath.values():
            caminho = item.get("PATH")
            if caminho and not isinstance(caminho, Path):
                item["PATH"] = Path(caminho)

    def importarMOD(self, listaMOD: list):
        try:
            self.listCarregar.clear()
            self.listSaida.clear()
            self.listLog.clear()

            inicio = time.perf_counter()
            
            modulos_executar = []
            for dic in listaMOD:
                for chave in dic.keys():
                    modulos_executar.append(dic[chave])

            totalList = len(modulos_executar)

            for fase, dadosModulo in enumerate(modulos_executar, 1):
                nomeModulo = dadosModulo.get('_Modulo')
                nomeClasse = dadosModulo.get('_classes')

                self.__AlimentarUI(fase=fase, total=totalList, modulo=nomeModulo, inicio=inicio)

                caminho = self.localMOD / f"{nomeModulo}.py"
                if not caminho.is_file():
                    msgbox.showerror(
                        "Erro de Módulo",
                        f"O arquivo '{nomeModulo}.py' não existe na pasta de execução:\n{self.localMOD}"
                    )
                    return None

                try:
                    nome_modulo_completo = f"mod.{nomeModulo}"
                    spec = importlib.util.spec_from_file_location(nome_modulo_completo, str(caminho))
                    if not (spec and spec.loader):
                        msgbox.showerror(
                            "Erro de Carregamento",
                            f"Não foi possível carregar as especificações do módulo '{nome_modulo_completo}'."
                        )
                        continue

                    moduloCarregado = importlib.util.module_from_spec(spec)
                    sys.modules[nome_modulo_completo] = moduloCarregado
                    spec.loader.exec_module(moduloCarregado)

                    if not hasattr(moduloCarregado, nomeClasse):
                        msgbox.showerror(
                            "Classe Não Encontrada",
                            f"A classe '{nomeClasse}' não foi localizada dentro do arquivo '{caminho.name}'."
                        )
                        continue

                    classe_bot = getattr(moduloCarregado, nomeClasse)
                    self.__TratarRota()
                    instancia = classe_bot(self.dictPath)

                    booleano = bool(instancia.pipeline())
                    carregado = []
                    saida = []

                    if booleano:
                        carregado = instancia.carregamento() or []
                        saida = instancia.Saida() or []

                        self.listCarregar.extend(carregado)
                        self.listSaida.extend(saida)

                    registro_modulo = {
                        "nome": nomeModulo,
                        "pipeline": "Finalizado" if booleano else "Erro",
                        "carregamento": "Finalizado" if carregado else "Vazio",
                        "retorno": "Finalizado" if saida else "Vazio"
                    }
                    self.listLog.append(registro_modulo)

                except Exception as e:
                    validador.registrar_log(e, f"Ponte -> {nomeModulo}")
                    self.listLog.append({
                        "nome": nomeModulo,
                        "pipeline": "Erro",
                        "carregamento": "Erro",
                        "retorno": "Erro"
                    })

            self.__RegistrarLogTabela(listaLogs=self.listLog)
            self.__MontarCarregamento(log=self.listCarregar)
            if self.listSaida:
                self.ancoraUI.contador.after(0, lambda: self.ancoraSaida.outputUI(self.listSaida))
        except Exception as e:
            validador.registrar_log(e, "Carregamento modulo")
            return None