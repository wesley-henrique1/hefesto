from src.lib.admDB import CRUD_DB, path_DB
from src.lib.executeBot import ExecuteBot
from src.lib.modErros import ModularErros
from src.lib.settings import _Icone

from tkinter import messagebox as msgbox
from pathlib import Path
from typing import Literal

import customtkinter as ctk
import pandas as pd
import threading
import math
import os

validador = ModularErros(fonte= "GUI - Bots")
class __auxiliares:
    def _CriarAncora(self):
        # Ancora do banco de dados das PATH(caminhos)
        rota = path_DB()
        dictRotas = rota.BuscarVlr()

        # Ancora do bando de dados dos bot
        radioVar = ctk.StringVar(value= "COMANDOS") 
        modulo = CRUD_DB(base= "bots")
        dicNome = modulo.BuscarVlr()

        MapaBox = []
        for chave in dicNome.keys():
            if  dicNome[chave]['_estado'] == '0':
                    continue
            MapaBox.append(
                {chave:{
                    "checkbox": int, 
                    "__estado__": radioVar, 
                    '_Nomenclatura': dicNome[chave]['_Nomenclatura']
                    }
                }
            )
        return dictRotas, MapaBox

    def _LimparWidget(self,tesk: str= Literal['disabled', 'normal'], listBT= list):
        try:
            for button in listBT:
                button.configure(state= tesk)
            self.Retorno.configure(fg_color= self.branco)
        except Exception as e:
            validador.registrar_log(e, "_LimparWidget")
    def _limpar_tela(self):
        try:
            self.contagem.configure(text="Total de Valores a serem processados: 000")
            self.contador.configure(text="Progresso: 000/000 |faltando: 000 |  00:00:00")
        
            self._desmarcar(listBT=[self.btIniciar, self.btLimpar])
            
            if hasattr(self, 'ModuloBot'):
                del self.ModuloBot
                
            self.continuar.configure(state='disabled')
            self.cancelar.configure(state='disabled')
            self.btAbrir.configure(state='normal')
        except Exception as e:
            validador.registrar_log(e, "_limpar_tela")
    def _desmarcar(self, listBT= list):
        try:
            self._LimparWidget(listBT= listBT, tesk= 'disabled')
            self.Retorno.configure(fg_color= self.branco)

            for dicionario in self.MapaBox:
                for registro in dicionario.keys():
                    dicionario[registro]['checkbox'].deselect()
        except Exception as e:
            validador.registrar_log(e, "_desmarcar")  
    def _puxarVlr(self, dictRota):
        try: 
            caminho = False
            for chave, dados in dictRota.items():
                if dados.get('VARIAVEL') == "_Saidas_":
                    caminho = Path(dados.get('PATH', ''))
                    break
            if not caminho:
                msgbox.showerror(
                    "Caminho de Saída Não Configurado",
                    "O diretório de output (saída) não foi definido nas configurações do sistema.\n\nPor favor, verifique o cadastro de rotas e caminhos antes de prosseguir."
                )
                return

            caminho.mkdir(parents=True, exist_ok=True)
            
            entrada = caminho / "EntradaBot.xlsx"
            saida = caminho / "SaidaBot.xlsx"
            return entrada, saida
        except Exception as e:
            validador.registrar_log(e, "_puxarVlr")  
    def _AbrirFile(self):
        try:
            if os.path.exists(self.entrada):
                os.remove(self.entrada)

            etapas = {
                'transferencia': ["CODPROD"],
                "Retirada": ['CODPROD', 'DTULTENT', 'QTESTGER', 'OBSFL'],
                'BOT3707': ["CODPROD", "DESTINO"],
                'Etapa_3': ["CODPROD", "PL_LASTRO", "PL", "CAP", "QTEnd", "V_CAP"],
                'adiconarPK': ["CODPROD", "DESTINO", 'CAPACIDADE', 'PONTO_REP']
            }
            with pd.ExcelWriter(self.entrada, engine='openpyxl') as writer:
                for nome_aba, colunas in etapas.items():
                    pd.DataFrame(columns=colunas).to_excel(writer, sheet_name=nome_aba, index=False)
            os.startfile(self.entrada)
        except Exception as e:
            validador.registrar_log(e, "_AbrirFile")  

        pass
    def _IniciosBot(self, root: ctk.CTk | ctk.CTkToplevel, mapa: list, rotas: dict):
        try:
            self.btAbrir.configure(state= 'disabled')
            chave_selecionada = None
            for dicionario in mapa:
                for chave in dicionario.keys():
                    estado_atual = dicionario[chave]['__estado__'].get()
                    if estado_atual == chave:
                        chave_selecionada = chave
                        break
                if chave_selecionada:
                    break

            if not chave_selecionada:
                msgbox.showwarning(
                    "Seleção Inválida",
                    "Nenhum módulo de automação foi selecionado.\n\nPor favor, marque um dos módulos na lista antes de tentar iniciar."
                )
                return
            if not self.entrada or not self.saida:
                msgbox.showwarning(
                    "Arquivos Não Encontrados",
                    "Nenhum arquivo de controle do bot foi gerado ou localizado.\n\nPor favor, certifique-se de que os arquivos de entrada e saída foram configurados corretamente antes de iniciar."
                )
                return

            def iniciar_execucao_background():
                self.ModuloBot = ExecuteBot(
                    UI= self,
                    chave=chave_selecionada, 
                    rotas=rotas,
                    entrada=self.entrada, 
                    saida=self.saida
                )
                valor_pipeline = self.ModuloBot.carregar_modulo()

                if valor_pipeline is not None:
                    self.continuar.configure(state= 'normal')
                    self.cancelar.configure(state= 'normal')

                else:
                    msgbox.showerror(
                        "Erro no Pipeline",
                        "Ocorreu uma falha durante a execução do pipeline do bot.\n\nVerifique os dados de entrada ou o log do sistema para mais detalhes."
                    )
            root.after(10, iniciar_execucao_background)
        except Exception as e:
            validador.registrar_log(e, "_IniciosBot")  
        pass
    
    def ClicarSimulador(self, contador: ctk.CTkLabel):
        try:
            if hasattr(self, 'ModuloBot') and self.ModuloBot:
                self.cancel_event = threading.Event()
                self.cancel_event.clear()
                self.after_id = None

                def fazer_contagem(segundos_restantes):
                    if self.cancel_event.is_set():
                        return
                    
                    if segundos_restantes > 0:
                        contador.configure(text=f"Iniciando em {segundos_restantes}...")          
                        self.after_id = contador.after(1000, lambda: fazer_contagem(segundos_restantes - 1))
                    else:
                        if self.cancel_event.is_set():
                            return
                            
                        contador.configure(text="Executando Simulador...")
                        
                        def rodar_thread_simulador():
                            self.ModuloBot.executar_simulador()
                            if not self.cancel_event.is_set():
                                contador.after(0, lambda: [
                                    self.continuar.configure(state='disabled'),
                                    self.cancelar.configure(state='disabled'),
                                    contador.configure(text="Simulação concluída!"),
                                    self.btAbrir.configure(state='normal')
                                ])
                        self.thread_simulador = threading.Thread(target=rodar_thread_simulador, daemon=True)
                        self.thread_simulador.start()
                fazer_contagem(5)
            else:
                msgbox.showwarning("Aviso", "Nenhum bot carregado para simular.")        
        except Exception as e:
            validador.registrar_log(e, "ao_clicar_em_simular")  

    def _cancelar_execucao(self):
        self.ModuloBot.Controladora(True)
        if hasattr(self, 'cancel_event'):
            self.cancel_event.set()
        if hasattr(self, 'after_id') and self.after_id:
            try:
                self.cancelar.after_cancel(self.after_id)
            except Exception:
                pass

        if hasattr(self, 'ModuloBot'):
            del self.ModuloBot
        
        self.continuar.configure(state='disabled')
        self.cancelar.configure(state='disabled')
        self.btAbrir.configure(state='normal')
        
        msgbox.showinfo(
            "Operação Cancelada",
            "A execução atual foi interrompida com sucesso a pedido do usuário."
        )
    pass
class BotsUI(__auxiliares):
    def __init__(self):
        self.familia = "Consolas"

        self.marromClaro = "#d8a859"
        self.vermelho = "#8e3312"
        self.branco = "#ffffff"
        self.marrom = "#8a541f"
        self.preto = "#000000"

        root = ctk.CTkToplevel()
        root.title("AUTOMAÇÃO")
        root.geometry("490x340")
        root.configure(fg_color=self.marromClaro)
        root.iconbitmap(_Icone.bigorna)
        root.resizable(False, False)

        self.dictRotas, self.MapaBox = self._CriarAncora()
        self.entrada, self.saida = self._puxarVlr(self.dictRotas)
        
        self.__Componentes(root)
        self.__clicaveis(root)
        self.__localizador()
        pass

    def __Componentes(self, tela):
        self.Painel = ctk.CTkFrame(
            tela,
            fg_color= self.branco,
            border_width= 3,
            border_color= self.preto,
        )
        self.Retorno = ctk.CTkFrame(
            tela,
            fg_color= self.branco,
            border_width= 3,
            border_color= self.preto,
        )

        self.contagem = ctk.CTkLabel(
             self.Retorno,
             text= "Total de Valores a serem processados: 000",
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            fg_color= self.branco,
            border_width= 3,
            border_color= self.preto,
        )
        
        self.contador = ctk.CTkLabel(
             self.Retorno ,
             text= "Progresso: 000/000 |faltando: 000 |  00:00:00",
            text_color= self.preto,

            font= (self.familia, 14, "bold"),
            fg_color= self.branco,
            border_width= 3,
            border_color= self.preto,
        )

        for dicionario in self.MapaBox:
            for registro in dicionario.keys():
                boxModulo = ctk.CTkRadioButton(
                    self.Painel,
                    text= dicionario[registro]['_Nomenclatura'],
                    value= registro,
                    variable= dicionario[registro]['__estado__'],

                    text_color= self.preto,
                    hover_color= self.vermelho,
                    fg_color= self.vermelho,
                    border_color= self.preto,
                    border_width_unchecked=3,

                    command= lambda: self._LimparWidget(listBT= [self.btIniciar, self.btLimpar], tesk= 'normal'),
                )
                dicionario[registro]['checkbox'] = boxModulo
        pass
    def __clicaveis(self, tela):
        self.btAbrir = ctk.CTkButton(
            self.Painel,
            text= "Abrir Arquivo",
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            text_color_disabled= self.vermelho,
            fg_color= self.branco,
            border_width= 3,
            command= self._AbrirFile
        )
        self.btIniciar = ctk.CTkButton(
            self.Painel,
            text= "Iniciar",
            state= 'disabled',
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            text_color_disabled= self.vermelho,
            fg_color= self.branco,
            border_width= 3,
            command= lambda: self._IniciosBot(mapa= self.MapaBox, rotas= self.dictRotas, root= tela)
        )
        self.btLimpar = ctk.CTkButton(
            self.Painel,
            text= "Limpar",
            state= 'disabled',
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            text_color_disabled= self.vermelho,
            fg_color= self.branco,
            border_width= 3,
            command= self._limpar_tela
        )
        self.desmarcar = ctk.CTkButton(
            self.Painel,
            text= "Desmarcar",
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            text_color_disabled= self.vermelho,
            fg_color= self.branco,
            border_width= 3,
            command= lambda: self._desmarcar(listBT= [self.btIniciar, self.btLimpar])
        )
        self.continuar = ctk.CTkButton(
            self.Retorno,
            text= "Continuar",
            state= 'disabled',
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            text_color_disabled= self.vermelho,
            fg_color= self.branco,
            border_width= 3,
            command=lambda: self.ClicarSimulador(contador= self.contador)
        )
        self.cancelar = ctk.CTkButton(
            self.Retorno,
            text= "Cancelar",
            state= 'disabled',
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            text_color_disabled= self.vermelho,
            fg_color= self.branco,
            border_width= 3,
            command= self._cancelar_execucao
        )
        pass
    def __localizador(self):
        self.Painel.place_configure(relx= 0.02, rely= 0.02, relheight= 0.40, relwidth= 0.96)
        self.Retorno.place_configure(relx= 0.02, rely= 0.44, relheight= 0.55, relwidth= 0.96)

        self.contagem.place_configure(relx= 0.02, rely= 0.04, relheight= 0.20, relwidth= 0.96)
        self.contador.place_configure(relx= 0.02, rely= 0.26, relheight= 0.20, relwidth= 0.96)

        self.btAbrir.place_configure(relx= 0.02, rely= 0.70, relheight= 0.20, relwidth= 0.30)
        self.btIniciar.place_configure(relx= 0.34, rely= 0.70, relheight= 0.20, relwidth= 0.20)
        self.btLimpar.place_configure(relx= 0.56, rely= 0.70, relheight= 0.20, relwidth= 0.20)
        self.desmarcar.place_configure(relx= 0.78, rely= 0.70, relheight= 0.20, relwidth= 0.20)

        self.continuar.place_configure(relx=0.275, rely=0.70, relheight=0.20, relwidth=0.20)
        self.cancelar.place_configure(relx=0.525, rely=0.70, relheight=0.20, relwidth=0.20)
        startX = 0.02
        startY = 0.06
        total = len(self.MapaBox)

        limite_coluna = math.ceil(total / 4)

        for index, dicionario in enumerate(self.MapaBox):
            for registro in dicionario.keys():
                
                dicionario[registro]['checkbox'].place(
                    rely=startY, relx=startX, relwidth=0.28, relheight=0.20
                )
                startY += 0.24
                if (index + 1) == limite_coluna:
                    startX = 0.34
                    startY = 0.06 
                elif (index + 1) == limite_coluna * 2:
                    startX = 0.66
                    startY = 0.06       
        pass
