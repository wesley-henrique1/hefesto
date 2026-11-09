import datetime as dt
from pathlib import Path
from tkinter import messagebox
import traceback
from src.lib import settings, admDB  #


class ModularErros:
    def __init__(self, e=None, etapas=None, fonte="ModuloExterno"):
        self.pasta_log: Path = settings._Caminho.PastaLog
        self.pasta_log.mkdir(parents=True, exist_ok=True)

        modulo = admDB.ErroDB() 
        bruto = modulo._conectar() 
        self.mapeamento = dict(bruto) if bruto else {} 
        self.fonte = fonte 

        if e is not None and etapas is not None: 
            self.registrar_log(e, etapas) 

    @property
    def __dtHoje(self) -> dt.date:
        return dt.date.today()

    def registrar_log(self, e, etapa):
        largura = 77 
        nome_do_erro = type(e).__name__ 
        msg = self.mapeamento.get(nome_do_erro, "Ocorreu um erro inesperado no sistema.") 
        agora = dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S') 
        
        rastro_tecnico = traceback.format_exc()
        if rastro_tecnico.strip() == "NoneType: None":
            rastro_tecnico = str(e)

        log_conteudo = (
            f"{'='* largura}\n"
            f"FONTE: {self.fonte} | ETAPA: {etapa} | DATA: {agora}\n"
            f"TIPO: {nome_do_erro}\n"
            f"MENSAGEM: {msg}\n"
            f"DETALHE TÉCNICO:\n{rastro_tecnico}\n"
            f"{'='* largura}\n\n"
        ) 

        try:
            data_str = self.__dtHoje.strftime("%Y-%m-%d")
            nome = f"Erros_{data_str}.txt"
            caminho = self.pasta_log / nome 

            with open(caminho, "a", encoding="utf-8") as f: 
                f.write(log_conteudo) 

            messagebox.showerror(
                "Falha na Execução",
                f"Erro na etapa: {etapa}\n\n{msg}\n\nDetalhes gravados em: {nome}"
            )
        except Exception as erro_f:
            messagebox.showerror("Log erros", f"Falha crítica ao gravar log: {erro_f}") 