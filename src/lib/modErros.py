import datetime as dt
from tkinter import messagebox
from src.lib.admDB import ErroDB

class ModularErros:
    def __init__(self, e=None, etapas=None, fonte="ModuloExterno"):
        modulo = ErroDB()
        bruto = modulo._conectar()
        self.mapeamento = dict(bruto) if bruto else {}
        self.fonte = fonte

        if e is not None and etapas is not None:
            self.registrar_log(e, etapas)
        pass

    def registrar_log(self, e, etapa):
        largura = 77
        nome_do_erro = type(e).__name__
        msg = self.mapeamento.get(nome_do_erro, "Ocorreu um erro inesperado no sistema.")
        agora = dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        
        log_conteudo = (
            f"{'='* largura}\n"
            f"FONTE: {self.fonte} | ETAPA: {etapa} | DATA: {agora}\n"
            f"TIPO: {nome_do_erro}\n"
            f"MENSAGEM: {msg}\n"
            f"DETALHE TÉCNICO: {e}\n"
            f"{'='* largura}\n\n"
        )
        try:
            with open("log_erros.txt", "a", encoding="utf-8") as f:
                f.write(log_conteudo)
            messagebox.showerror("Log erros", log_conteudo)
        except Exception as erro_f:
            messagebox.showerror("Log erros", f"Falha crítica ao gravar log: {erro_f}")
