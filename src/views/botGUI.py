import sys
from pathlib import Path

file_path = Path(__file__).resolve()
src_path = file_path.parents[1]
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))

from lib.admDB import CRUD_DB, path_DB
from lib.executeBot import ExecuteBot

from tkinter import messagebox as msgbox
import customtkinter as ctk
import pandas as pd
import math
import os

class __auxiliares:
    def _LimparWidget(self,tesk: str= 'disabled' | 'normal', listBT= list):
        try:
            for button in listBT:
                button.configure(state= tesk)
            self.Retorno.configure(fg_color= self.branco)
        except Exception as e:
            print(e)
            # validador.registrar_log(e, "_LimparWidget")
    def _desmarcar(self, listBT= list):
        try:
            self._LimparWidget(listBT= listBT, tesk= 'disabled')
            self.Retorno.configure(fg_color= self.branco)

            for dicionario in self.MapaBox:
                for registro in dicionario.keys():
                    dicionario[registro]['checkbox'].deselect()
        except Exception as e:
            print(e)
            # validador.registrar_log(e, "_desmarcar")  
    def _AbrirFile(self, dictRota: dict):
        try: 
            for chave, dados in dictRota.items():
                if dados.get('VARIAVEL') == "_OutPut_":
                    caminho = Path(dados.get('PATH', ''))
                    break
            if not caminho:
                print("Erro: Caminho de output não foi configurado.")
                return

            caminho.mkdir(parents=True, exist_ok=True)
            
            Saida = caminho / "SaidaBot.xlsx"
            Entrada = caminho / "EntradaBot.xlsx"
        except Exception as e:
            Entrada = r'c:\Users\User\Desktop\saida_codigos\EntradaBot.xlsx'
            Saida = pd.DataFrame()
            print("Erro", e)

        if os.path.exists(Entrada):
            os.remove(Entrada)
            print(f"Arquivo {Entrada.name} apagado com sucesso.")

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
        os.startfile(Entrada)

        return Entrada, Saida 
    def _IniciosBot(self,root: ctk.CTk | ctk.CTkToplevel, mapa: list, rotas: dict):
        chave_selecionada = None
        for dicionario in mapa:
            for chave in dicionario.keys():
                estado_atual = dicionario[chave]['__estado__'].get()
                if estado_atual == chave:
                    chave_selecionada = chave
                    print(f"\n>> Modulo selecionado para iniciar: {chave_selecionada}\n")  
                    break
            if chave_selecionada:
                break
        if not chave_selecionada:
            msgbox.showwarning("Aviso", "Nenhum modulo selecionado")
            print("\n>> Nenhum modulo selecionado")
            return
        arquivoEntrada, arquivoSaida = self._AbrirFile(rotas)
        root.after(10, lambda: ExecuteBot(
            chave= chave_selecionada, 
            rotas= rotas,
            entrada= arquivoEntrada, 
            saida= arquivoSaida
        ))
        pass
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

class BotsUI(__auxiliares):
    def __init__(self):
        self.familia = "Consolas"

        self.marromClaro = "#d8a859"
        self.vermelho = "#8e3312"
        self.branco = "#ffffff"
        self.marrom = "#8a541f"
        self.preto = "#000000"

        root = ctk.CTk()
        root.title("AUTOMAÇÃO")
        root.geometry("440x300")
        root.configure(fg_color=self.marromClaro)
        # root.iconbitmap(_Icone.perfil)
        root.resizable(False, False)

        self.dictRotas, self.MapaBox = self._CriarAncora()
        
        self.__Componentes(root)
        self.__clicaveis()
        self.__localizador()

        root.mainloop()
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

                    command= lambda: self._LimparWidget(listBT= [self.btIniciar, self.btParar], tesk= 'normal'),
                )
                dicionario[registro]['checkbox'] = boxModulo
        pass
    def __clicaveis(self):
        self.btAbrir = ctk.CTkButton(
            self.Painel,
            text= "Abrir Arquivo",
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            text_color_disabled= self.vermelho,
            fg_color= self.branco,
            border_width= 3,
            command= lambda: self._AbrirFile(self.dictRotas)
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
            command= lambda: self._IniciosBot(mapa= self.MapaBox, rotas= self.dictRotas)
        )
        self.btParar = ctk.CTkButton(
            self.Painel,
            text= "Parar",
            state= 'disabled',
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            text_color_disabled= self.vermelho,
            fg_color= self.branco,
            border_width= 3,
            # command= self.FUNC_demandas
        )
        self.desmarcar = ctk.CTkButton(
            self.Painel,
            text= "Desmarcar",
            font= (self.familia, 14, "bold"),
            text_color= self.preto,
            text_color_disabled= self.vermelho,
            fg_color= self.branco,
            border_width= 3,
            command= lambda: self._desmarcar(listBT= [self.btIniciar, self.btParar])
        )
        pass
    def __localizador(self):
        self.Painel.place_configure(relx= 0.02, rely= 0.02, relheight= 0.40, relwidth= 0.96)
        self.Retorno.place_configure(relx= 0.02, rely= 0.44, relheight= 0.55, relwidth= 0.96)

        self.contagem.place_configure(relx= 0.02, rely= 0.04, relheight= 0.20, relwidth= 0.96)
        self.contador.place_configure(relx= 0.02, rely= 0.26, relheight= 0.20, relwidth= 0.96)

        self.btAbrir.place_configure(relx= 0.02, rely= 0.70, relheight= 0.20, relwidth= 0.30)
        self.btIniciar.place_configure(relx= 0.34, rely= 0.70, relheight= 0.20, relwidth= 0.20)
        self.btParar.place_configure(relx= 0.56, rely= 0.70, relheight= 0.20, relwidth= 0.20)
        self.desmarcar.place_configure(relx= 0.78, rely= 0.70, relheight= 0.20, relwidth= 0.20)

        startX = 0.02
        startY = 0.06
        total = len(self.MapaBox)

        limite_coluna = math.ceil(total / 2)

        for index, dicionario in enumerate(self.MapaBox):
            for registro in dicionario.keys():
                
                dicionario[registro]['checkbox'].place(
                    rely=startY, relx=startX, relwidth=0.40, relheight=0.20
                )
                startY += 0.22
                if (index + 1) == limite_coluna:
                    startX = 0.35
                    startY = 0.06 
                elif (index + 1) == limite_coluna * 2:
                    startX = 0.68
                    startY = 0.06       
        pass


if __name__ == "__main__":
    BotsUI()